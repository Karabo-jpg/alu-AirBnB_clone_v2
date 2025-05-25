#!/usr/bin/python3
"""Tests for Place class."""
import unittest
from models.place import Place
from datetime import datetime


class TestPlace(unittest.TestCase):
    """Test cases for the Place class."""

    def setUp(self):
        """Set up before each test."""
        self.place = Place()

    def test_init(self):
        """Test initialization of Place."""
        self.assertIsInstance(self.place.id, str)
        self.assertIsInstance(self.place.created_at, datetime)
        self.assertIsInstance(self.place.updated_at, datetime)
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")

    def test_attributes(self):
        """Test place attributes."""
        self.place.city_id = "123"
        self.place.user_id = "456"
        self.place.name = "Cozy Cabin"
        self.assertEqual(self.place.city_id, "123")
        self.assertEqual(self.place.user_id, "456")
        self.assertEqual(self.place.name, "Cozy Cabin")

    def test_str(self):
        """Test string representation of Place."""
        expected = f"[Place] ({self.place.id}) {self.place.__dict__}"
        self.assertEqual(str(self.place), expected)

    def test_save(self):
        """Test save method updates updated_at."""
        old_updated_at = self.place.updated_at
        self.place.save()
        self.assertNotEqual(old_updated_at, self.place.updated_at)

    def test_to_dict(self):
        """Test to_dict method creates a dictionary with correct attributes."""
        place_dict = self.place.to_dict()
        self.assertEqual(place_dict['__class__'], 'Place')
        self.assertEqual(place_dict['id'], self.place.id)
        self.assertEqual(place_dict['created_at'],
                         self.place.created_at.isoformat())
        self.assertEqual(place_dict['updated_at'],
                         self.place.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
