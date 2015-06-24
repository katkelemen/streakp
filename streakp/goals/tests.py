from django.test import TestCase

# Create your tests here.
from django.utils import unittest
from streak import get_streak, dates_to_ints, cons_dates
from datetime import datetime


class StreakTest(unittest.TestCase):

    def test_cons_dates(self):
        dates = [datetime(1987,9,24),
                 datetime(1987, 8, 21),
                 datetime(1987, 8, 22)]
        self.assertEqual(cons_dates(dates), 2)