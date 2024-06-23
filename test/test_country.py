#!/usr/bin/python3
"""Unittest for Country"""

import unittest
from model.country import Country


class TestCountry(unittest.TestCase):

    def setUp(self):
        self.country = Country(name="Testland")

    def test_initialization(self):
        self.assertEqual(self.country.name, "Testland")
        self.assertEqual(self.country.states, [])

    def test_add_state(self):
        self.country.add_state("State1")
        self.assertIn("State1", self.country.states)
        self.assertEqual(len(self.country.states), 1)

    def test_add_duplicate_state(self):
        self.country.add_state("State1")
        self.country.add_state("State1")
        self.assertEqual(self.country.states.count("State1"), 1)

    def test_remove_state(self):
        self.country.add_state("State1")
        self.country.remove_state("State1")
        self.assertNotIn("State1", self.country.states)
    
     def test_str_representation(self):
        self.country.add_state("State1")
        self.country.add_state("State2")
        expected_str = f"Country(ID: {self.country.id}, Name: Testland, States: [State1, State2])"
        self.assertEqual(str(self.country), expected_str)
        if __name__ == '__main__':
            unittest.main()
