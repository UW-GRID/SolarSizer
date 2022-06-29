"""
PySAM submodule that runs the main pvmodel
This module requires the irradiance data and user input text
    file to be saved within the data directory
"""

import os
import numpy as np
import PySAM.Pvsamv1 as pv

def execute_pvmodel(number_of_modules_per_string, number_of_strings, n_inverters=4):
    """
    Function that executes the pvmodel

    Parameters:
        number_of_modules_per_string (int):Number of panels wired in series
        number_of_strings (int):Number of strings wired in parallel
        n_inverters (int):Number of inverters

    Returns:
        pvmodel (obj):Represents solar array for current parameters
        our_load_profile (txt):The user input load profile used to execute the pvmodel
    """

    if number_of_modules_per_string>7:
        raise AssertionError('Number of modules per string exceeds limit of 7')
    if number_of_strings>30:
        raise AssertionError('Number of string exceeds limit of 30')
    if n_inverters>number_of_strings:
        raise AssertionError('Number of inverters exceeds number of strings')
    data_path = os.path.abspath("../solarsizer/data")

    # initialize model with defaults
    pvmodel = pv.default('PVBatteryResidential')

    # sepcify solar resource file for the location
    pvmodel.SolarResource.solar_resource_file = os.path.join(data_path, "irradiance.epw")

    print('found irradiance.epw')
    print(os.path.join(data_path, "irradiance.epw"))

    # try user load profile. Removed try excepts for now.
    our_load_profile = np.loadtxt(os.path.join(data_path, "user_load_profile.txt"), skiprows=0)

    print('user load profile loaded')
    print(os.path.join(data_path, "user_load_profile.txt"))

    #except:
        # add exception
       # our_load_profile = np.loadtxt(os.path.join(data_path,
       #    "Max_load_profile_for_year.txt"), skiprows=1)
       # print('user load profile did not work. Using default load profile')
       # print(os.path.join(data_path, "Max_load_profile_for_year.txt"))

    pvmodel.Load.load = tuple(our_load_profile)

    print('loaded load profile')

    # select module and inverter from database
    pvmodel.Module.module_model = 1 # set it to CEC model

    pvmodel.Inverter.inverter_model = 0. # set it to CEC
    pvmodel.Inverter.inv_num_mppt = 1 # use single mmpts

    ## Max number of modules in a string
    max_modules_in_string = pvmodel.Inverter.mppt_hi_inverter/pvmodel.CECPerformanceModelWithModuleDatabase.cec_v_oc_ref

    ## Min number of modules in a string
    min_modules_in_string = pvmodel.Inverter.mppt_low_inverter/pvmodel.CECPerformanceModelWithModuleDatabase.cec_v_oc_ref

    print('set some parameters and got min and max modules')

    # modules per string specified must be within (min, max) modules required
    assert number_of_modules_per_string > min_modules_in_string
    assert number_of_modules_per_string < max_modules_in_string

    print('min and max modules check passsed')

    # System Design
    pvmodel.SystemDesign.inverter_count = n_inverters

    pvmodel.SystemDesign.subarray1_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray1_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray1_mppt_input = 1
    pvmodel.SystemDesign.subarray1_track_mode = 0 # fixed tracking

    pvmodel.SystemDesign.subarray2_enable = 1
    pvmodel.SystemDesign.subarray2_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray2_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray2_mppt_input = 1
    pvmodel.SystemDesign.subarray2_track_mode = 0 # fixed tracking

    pvmodel.SystemDesign.subarray3_enable = 1
    pvmodel.SystemDesign.subarray3_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray3_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray3_mppt_input = 1
    pvmodel.SystemDesign.subarray3_track_mode = 0 # fixed tracking

    pvmodel.SystemDesign.subarray4_enable = 1
    pvmodel.SystemDesign.subarray4_modules_per_string = number_of_modules_per_string
    pvmodel.SystemDesign.subarray4_nstrings = number_of_strings
    pvmodel.SystemDesign.subarray4_mppt_input = 1
    pvmodel.SystemDesign.subarray4_track_mode = 0 # fixed tracking

    print('something System Design')

    # Total Capacity of the system
    mod_power_rating = pvmodel.CECPerformanceModelWithModuleDatabase.cec_v_mp_ref * pvmodel.CECPerformanceModelWithModuleDatabase.cec_i_mp_ref
    pvmodel.SystemDesign.system_capacity = mod_power_rating * 4 * number_of_modules_per_string * number_of_strings

    print('something Total Capacity of the system')

    # Battery system design - charge/discharge
    pvmodel.BatterySystem.batt_current_charge_max = 24
    pvmodel.BatterySystem.batt_current_discharge_max = 24

    pvmodel.BatterySystem.batt_power_charge_max_kwac = 12
    pvmodel.BatterySystem.batt_power_discharge_max_kwac= 11

    pvmodel.BatterySystem.batt_power_charge_max_kwdc = 12
    pvmodel.BatterySystem.batt_power_discharge_max_kwdc= 12

    print('something Battery system design')

    # MUST ENABLE Battery storage!!
    pvmodel.BatterySystem.en_batt = 1

    # Battery Dispatch
    pvmodel.BatteryDispatch.batt_dispatch_choice = 4.0 # manual discharge
    pvmodel.BatteryDispatch.dispatch_manual_charge = (1, 1, 1, 1, 0, 0)
    pvmodel.BatteryDispatch.dispatch_manual_discharge = (1, 1, 1, 1, 0, 0)
    pvmodel.BatteryDispatch.dispatch_manual_percent_discharge = (25, 25, 25, 75)

    print('about to execute model')

    # Finally, run the model!
    pvmodel.execute()

    print('done executing the model')

    return pvmodel, our_load_profile
