#!/usr/bin/python3
"""Tests for Review class."""
import unittest
from models.review import Review
from datetime import datetime


class TestReview(unittest.TestCase):
    """Test cases for the Review class."""

    def setUp(self):
        """Set up before each test."""
        self.review = Review()

    def test_init(self):
        """Test initialization of Review."""
        self.assertIsInstance(self.review.id, str)
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsInstance(self.review.updated_at, datetime)
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_attributes(self):
        """Test review attributes."""
        self.review.place_id = "123"
        self.review.user_id = "456"
        self.review.text = "Great stay!"
        self.assertEqual(self.review.place_id, "123")
        self.assertEqual(self.review.user_id, "456")
        self.assertEqual(self.review.text, "Great stay!")

    def test_str(self):
        """Test string representation of Review."""
        expected = f"[Review] ({self.review.id}) {self.review.__dict__}"
        self.assertEqual(str(self.review), expected)

    def test_save(self):
        """Test save method updates updated_at."""
        old_updated_at = self.review.updated_at
        self.review.save()
        self.assertNotEqual(old_updated_at, self.review.updated_at)

    def test_to_dict(self):
        """Test to_dict method creates a dictionary with correct attributes."""
        review_dict = self.review.to_dict()
        self.assertEqual(review_dict['__class__'], 'Review')
        self.assertEqual(review_dict['id'], self.review.id)
        self.assertEqual(review_dict['created_at'],
                         self.review.created_at.isoformat())
        self.assertEqual(review_dict['updated_at'],
                         self.review.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
