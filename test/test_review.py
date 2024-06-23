#!/usr/bin/python3
"""Unittest for Review"""


import unittest
from datetime import datetime
from model.review import Review


class TestReview(unittest.TestCase):

    def setUp(self):
        """Setup a default Review instance for testing."""
        self.review = Review(
            user="Test User",
            place="Test Place",
            text="Great place to stay!",
            rating=5
        )

    def test_review_creation(self):
        """Test that a Review instance is created correctly."""
        self.assertEqual(self.review.user, "Test User")
        self.assertEqual(self.review.place, "Test Place")
        self.assertEqual(self.review.text, "Great place to stay!")
        self.assertEqual(self.review.rating, 5)
        self.assertIsNotNone(self.review.id)
        self.assertIsInstance(self.review.create_time, datetime)
        self.assertIsInstance(self.review.update_time, datetime)

    def test_update_review(self):
        """Test updating the attributes of a review."""
        previous_update_time = self.review.update_time
        self.review.update(text="Amazing experience!", rating=4)
        self.assertEqual(self.review.text, "Amazing experience!")
        self.assertEqual(self.review.rating, 4)
        self.assertNotEqual(self.review.update_time, previous_update_time)

