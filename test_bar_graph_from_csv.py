""""Salvatore Rosa

Unit Tests
----------

Written with Python 3.7.x.
Should work with the latest Python as well.

To run unit tests in terminal:
>python -m unittest test_bar_graph_from_csv.py
"""

import unittest
from typing import List
import csv

from bar_graph_from_csv import (
    get_columns,
    Column,
    get_largest_value,
    get_smallest_value,
    get_largest_end_point,
    get_smallest_end_point,
    get_left_margin_space,
)


class TestBarGraphFromCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("test-data.csv", newline="") as file:
            cls.reader = csv.reader(file, dialect="excel")
            cls.columns = get_columns(cls.reader)

    def test_get_columns_returns_list(self):
        self.assertIsInstance(self.columns, List)

    def test_get_empty_columns_returns_a_list_with_expected_length(self):
        self.assertEqual(len(self.columns), 3)

    def test_get_empty_columns_returns_list_of_columns(self):
        for item in self.columns:
            self.assertIsInstance(item, Column)

    def test_get_empty_columns_returns_list_of_columns_with_expected_data(self):
        self.assertEqual(self.columns[0].name, "year")
        self.assertEqual(self.columns[0].data, ["1900", "1910", "1920", "1930", "1940"])
        self.assertEqual(self.columns[1].name, "profit")
        self.assertEqual(self.columns[1].data, ["20", "25", "40", "-5", "5"])
        self.assertEqual(self.columns[2].name, "employees")
        self.assertEqual(self.columns[2].data, ["3", "4", "10", "6", "6"])

    def test_get_largest_value_returns_int(self):
        self.assertIsInstance(get_largest_value(self.columns[1:]), int)

    def test_get_largest_value_returns_expected_value(self):
        self.assertEqual(get_largest_value(self.columns[1:]), 40)

    def test_get_smallest_value_returns_int(self):
        self.assertIsInstance(get_smallest_value(self.columns[1:]), int)

    def test_get_smallest_value_returns_expected_value(self):
        self.assertEqual(get_smallest_value(self.columns[1:]), -5)

    def test_get_largest_end_point_returns_int(self):
        self.assertIsInstance(get_largest_end_point(15, self.columns[1:]), int)

    def test_get_largest_end_point_returns_expect_value(self):
        print(self.columns[1:])
        self.assertEqual(get_largest_end_point(15, self.columns[1:]), 60)

    def test_get_smallest_end_point_returns_int(self):
        self.assertIsInstance(get_smallest_end_point(15, self.columns[1:]), int)

    def test_get_smallest_end_point_returns_expect_value(self):
        print(self.columns[1:])
        self.assertEqual(get_smallest_end_point(15, self.columns[1:]), -15)

    def test_get_left_margin_space_returns_int(self):
        self.assertIsInstance(get_left_margin_space(self.columns[0]), int)

    def test_get_left_margin_space_returns_expected_value(self):
        self.assertEqual(get_left_margin_space(self.columns[0]), 4)


if __name__ == "__main__":
    unittest.main()
