"""
Module that contains function to convert GUI input file to a dataframe
Saves the dataframe to a txt file within the data directory

We assume the input file is csv format

"""

import numpy as np

def create_load_txt(data):
    """
    Loads in pandas dataframe containing load profile from GUI.
    Then gets the row with the hourly load and saves as a txt file
    to be used in the PySAM model.
    The txt file contains the daily load profile repeated
    for a year and is named 'user_load_profile.txt'.
    This txt file is saved within the data directory.

    Parameters:
        data (pandas dataframe):A dataframe containing the file contents of the load profile csv

    """

    # get load row
    load_row_day = data.iloc[-2]

    # get rid of nans and get values
    load_row_day = load_row_day.dropna()

    load_row_day = load_row_day.values

    # drop peak and total load
    load_row_day = load_row_day[1:-1]

    # raise type error is all values in array are not floats or ints.
    # WHY ARE they objects right now:
#    try:
#        # try changing each value in array to an int. If it does not work, raise type error
#        for myVariable in load_row_day:
#            print(myVariable)
#            print(type(myVariable))
#            myVariable = int(myVariable)
#            print(myVariable)
#    except:
#        raise TypeError('The load profile must contain only numerical values')

    # raise value error if load profile is not the correct length
    if len(load_row_day) != 24:
        raise ValueError('The load profile has the wrong number of load values. Please make sure you have load values for 24 hours')

    # raise value error is one or more nans are in array
#    if np.isnan(np.sum(load_row_day)) == True:
#        raise ValueError('The load profile cannot contain nans')

    # don't raise any exceptions if load_row_day meets the criteria
    else:
        pass

    # assuming constant load for each day, create load profile for year
    load_row_year = np.array([load_row_day]*365)
    load_row_year = load_row_year.astype(dtype='float')
    load_row_year = np.reshape(load_row_year, (365*24))

    load_row_year_kw = load_row_year/1000 # converts from watts to kW


    np.savetxt('data/user_load_profile.txt', load_row_year_kw, delimiter=' ')
