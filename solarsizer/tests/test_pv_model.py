"""
Module to test the pv model
"""

import unittest

from pysam.pysam_utils import run_pvmodel

class TestPVModel(unittest.TestCase):
    """
    Running tests on the pv_model.py module
    """
    @classmethod
    def test_smoke(cls):
        """
        Simple smoke test to make sure function runs.
        """
        run_pvmodel.execute_pvmodel(5, 6, n_inverters=6)

# One shot: In this case, you call the code under test with arguments
#    for which you know the expected result
#    1. We could do this with the above smoke test or create
#       another set up where we know the output

    def test_too_many_modules_per_string(self):
        """
        Edge test to make sure the function throws an error
        when too modules per string
        """
        number_of_modules_per_string = 8
        number_of_strings = 6
        n_inverters = 6

        with self.assertRaises(AssertionError):
            run_pvmodel.execute_pvmodel(number_of_modules_per_string,
                    number_of_strings, n_inverters)

    def test_too_many_string(self):
        """
        Edge test to make sure the function throws an error
        when too modules per string
        """
        number_of_modules_per_string = 7
        number_of_strings = 31
        n_inverters = 30

        with self.assertRaises(AssertionError):
            run_pvmodel.execute_pvmodel(number_of_modules_per_string,
                    number_of_strings, n_inverters)

    def test_too_many_inverters(self):
        """
        Edge test to make sure the function throws an error
        when too modules per string
        """
        number_of_modules_per_string = 6
        number_of_strings = 30
        n_inverters = 31

        with self.assertRaises(AssertionError):
            run_pvmodel.execute_pvmodel(number_of_modules_per_string,
                    number_of_strings, n_inverters)

# Edge test: The code under test is invoked with arguments that should
#    cause an exception, and you evaluate if the expected exception occurs
#    1. 1-7 panels in string, 1-30 strings, 1-30 inverters

# Pattern test: Based on your knowledge of the *calculation*
#    (not implementation) of the code under test, you construct a
#    suite of test cases for which the results are known or there
#    are known patterns in these results that are used to evaluate
#    the results returned
#    1. Run twice with different number of panels, array with more
#       panels should have greater uptime percentage
