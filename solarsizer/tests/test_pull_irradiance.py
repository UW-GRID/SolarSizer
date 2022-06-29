"""
Module to test pull_irradiance
"""

import unittest

from utils import pull_irradiance

class Testpullirradiance(unittest.TestCase):
    """
    Testing the pull_irradiance.py module
    """

    @classmethod
    def test_smoke(cls):
        """
        Simple smoke test to make sure function runs.
        """
        pull_irradiance.create_irradiance_file(43, -122)

    @classmethod
    def test_oneshot(cls):
        """
        One shot test
        """
        pull_irradiance.create_irradiance_file(45, -122)

    def test_invalid_lat_lon_year(self):
        """
        Edge test to make sure the function throws an error
        Should says invalue inputs: lat, lon or year
        We can probably just let these errors be caught by one error
        unless we know the bounds of the data and want to catch them
        before calling the API
        """
        with self.assertRaises(AssertionError):
            pull_irradiance.create_irradiance_file(122, -222)
