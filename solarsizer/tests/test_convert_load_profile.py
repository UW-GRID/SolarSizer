"""
Module to test convert_load_profile
"""

import unittest

import pandas as pd

from utils import convert_load_profile

class Testconvertloadprofile(unittest.TestCase):
    """
    Testing the convert_load_profile.py module
    """

    @classmethod
    def test_smoke(cls):
        """
        Simple smoke test to make sure function runs.
        """
        data = pd.read_csv(r'tests/test_data/load_profile_smoke.csv')

        convert_load_profile.create_load_txt(data)

    @classmethod
    def test_oneshot(cls):
        """
        One shot test
        """
        data = pd.read_csv(r'tests/test_data/load_profile_one_shot.csv')

        convert_load_profile.create_load_txt(data)

        # ADD CODE to compare txts created to correct txt

    def test_wrong_len_load_row_day(self):
        """
        Edge test to make sure the function throws an error
        when load_row_day does not have a length of 24
        """
        data = pd.read_csv(r'tests/test_data/load_profile_too_many_hours.csv')

        with self.assertRaises(ValueError):
            convert_load_profile.create_load_txt(data)


# Additional tests to run on array load_row_day. These cannot
#    be run right now as dtype comes in as object.
#
# Ideally dtype should match data type (e.g. float, int, str)
#    so that data type can be checked.
#
# The pysam model takes in a load profile txt of values.
#
# See lines 36-45 and 51-53 of convert_load_profile.py for
#    exceptions to pass these tests.
#
#    def test_not_values_load_row_day(self):
#        """
#        Edge test to make sure the function throws an error
#        when load_row_day is not floats or ints
#        """
#        data = pd.read_csv(r'test_data/load_profile_some_loads_are_strings.csv')
#
#        with self.assertRaises(TypeError):
#            convert_load_profile.create_load_txt(data)
#        return
#    def test_NaN_in_load(self):
#        """
#        Edge test to make sure the function throws an error
#        when Nans are in the load profile
#        """
#        data = # need to make test data
#
#        with self.assertRaises(ValueError):
#            convert_load_profile.create_load_txt(data)
#        return
