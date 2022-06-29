"""
Module that contains the PySAM model

Workflow for running PySAM:
- Instantiate the model with default values
- Specify the solar resource file for the location
- Assign the load profile (defined above) to the the model.
  This will inform the model what kind of load our system will support
- Pick module and inverter models - can design our own with specifications as
  needed but here we will pick from the available database
- Identify the minimum and the maximum number of modules that can be in a string
  (*connected in series*). This is to make sure we are in the operating range for
  the inverter. The number of modules we select to be connected in a string must
  fall between these min and max values
- Design the system :
    - Set inverter count - *how many inverters do we want?*
    - For a single subarray:
        - Assign the number of modules in a string (*modules in series*)
        - Assign the number of strings (*rows (in parallel)*)
        - Fixed axis system or tracking
          (*tracking means it will track the sun throughout the day*)
    - Repeat for desired number of subarrays
- Specify Battery system specs: charge, discharge
- Identify power dispatch from battery
    - Manually control - specify when to charge and discharge the battery
      (*this makes more sense if you look at the UI in SAM*)
- Execute the model!

Refer to this link:
https://sam.nrel.gov/images/webinar_files/sam-webinars-2020-modeling-pv-systems.pdf
for detailed explanation on MMPT, subarray, strings, etc
"""

import numpy as np
import pandas as pd
from pysam.pysam_utils import run_pvmodel

def pysam_model():
    """
    Function that runs PySAM

    There are no input parameters, but ensure you have a
    txt load profile and an irradiance csv file within the data directory

    Returns:
        df_system_array (df):Pandas dataframe that contains component information
    """
    print('started running')

    ## Running single scenario to get an estimate of the array size
    pv_guess, our_load_profile = run_pvmodel.execute_pvmodel(2, 1, n_inverters=1)

    print('calculating uptime_hours')

    uptime_hours = np.count_nonzero(
        (np.array(pv_guess.Outputs.system_to_load) +
         np.array(pv_guess.Outputs.batt_to_load) -
         np.tile(our_load_profile, 25)  # repeat load profile for 25 years
        ) == 0
    )

    print('calculating panel_number_estimate')

    # Uptime hours and percent uptime for 25 years
    panel_number_estimate = (1/(uptime_hours/(365 * 24 * 25)))/1.5

    print('panel_number_estimate', panel_number_estimate)


    # Now, we will evaluate multiple scenarios - we will look at a
    #     range of modules numbers and a range of strings to find minimum
    #     system requirements that satisfy maximum uptime

    pvmodels_param = []
    pvmodels = []

    print('testing multiple scenarios')

    for mod in range(2,8): # mod is no of modules
        for no_str in range(1,30): # no_str is no of strings
            # print('m', mod)
            # print('n',no_str)
            if mod*no_str >=panel_number_estimate:
                print('mod*no_str is greater than panel_number_estimate')
                pvarray, our_load_profile = run_pvmodel.execute_pvmodel(mod,no_str,mod)
                pvmodels_param.append([mod, no_str, no_str])
                pvmodels.append(pvarray)
                print('scenario ran')

#    if len(pvmodels) == 0:
#    #error for system cant match load profile
#        pass

    uptime_percent = []
    pvmodel_analysis = []
    system_analysis = []

    print('pvmodels', pvmodels)

    for i in range(len(pvmodels)):
        uptime_hours = np.count_nonzero(
            (np.array(pvmodels[i].Outputs.system_to_load) +
             np.array(pvmodels[i].Outputs.batt_to_load) -
             np.tile(our_load_profile, 25)  # repeat load profile for 25 years
            ) == 0
        )

        print('uptime_hours', uptime_hours)

        uptime_percent.append(uptime_hours/(365 * 24 * 25))
        print('uptime_percent', uptime_percent)
        pvmodel_analysis = pvmodels_param[i]
        print('pvmodel_analysis', pvmodel_analysis)
        pvmodel_analysis.append(uptime_percent[i])
        print('pvmodel_analysis', pvmodel_analysis)
        system_analysis.append(pvmodel_analysis)
        print('system_analysis', system_analysis)

    print('out of loop')
    df_system_array = pd.DataFrame(
            system_analysis,columns =
            ['Panels in Strings','Strings','Inverters','Uptime_Percent'])

    print('df_system_array', df_system_array)
    #df_uptime_met = df_system_array[df_system_array.Uptime_Percent>0.95]

    print('finished running')

    return df_system_array
