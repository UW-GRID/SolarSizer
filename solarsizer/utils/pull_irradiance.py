"""
Module to pull irradiance from database using an API
Irradiance is retrieved from the ECMWF database (add link)

Note: The API has limited uses per day. If you have an API error,
refresh the page and try again.
"""

import urllib.request
import os

def create_irradiance_file(lat, lon):
    """
    Function that creates API and pulls irradiance data for given latitude and longitude
    The irradiance data as a csv file named 'irradiance.csv' within the data directory
    This function has no returns

    Parameters:
        lat (float):latitude input from GUI
        lon (float):longitude input from GUI

    """

    # Declare url string
    url = 'https://re.jrc.ec.europa.eu/api/tmy?lat={lat}&lon={lon}&outputformat=epw'.format(lat=lat, lon=lon)
    data_path = os.path.abspath('../solarsizer/data')

    try:
        _ = urllib.request.urlretrieve(url, data_path + '/irradiance.epw')
        # add exception for multiple API call
    except:
        raise AssertionError('No irradiance data found for latitude and longintude')
