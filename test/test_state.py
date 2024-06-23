#!/usr/bin/python3
"""Unittest for State"""

import unittest
from datetime import datetime
from model.state import State

class TestState(unittest.TestCase):

    def setUp(self):
        """Setup a default State instance for testing."""
        self.state = State(
            name="Test State",
            country="Test Country"
        )

    def test_state_creation(self):
        """Test that a State instance is created correctly."""
        self.assertEqual(self.state.name, "Test State")
        self.assertEqual(self.state.country, "Test Country")
        self.assertIsNotNone(self.state.id)
        self.assertIsInstance(self.state.create_time, datetime)
        self.assertIsInstance(self.state.update_time, datetime)

    def test_add_city(self):
        """Test adding cities to a state."""
        self.state.add_city("Test City")
        self.assertIn("Test City", self.state.cities)

    def test_remove_city(self):
        """Test removing cities from a state."""
        self.state.add_city("Test City")
        self.state.remove_city("Test City")
        self.assertNotIn("Test City", self.state.cities)

    def test_update_attributes(self):
        """Test updating the attributes of a state."""
        self.state.update(name="Updated State", country="Updated Country")
        self.assertEqual(self.state.name, "Updated State")
        self.assertEqual(self.state.country, "Updated Country")
