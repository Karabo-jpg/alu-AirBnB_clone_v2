#!/usr/bin/python3
"""Tests for Amenity class."""
import unittest
from models.amenity import Amenity
from datetime import datetime


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class."""

    def setUp(self):
        """Set up before each test."""
        self.amenity = Amenity()

    def test_init(self):
        """Test initialization of Amenity."""
        self.assertIsInstance(self.amenity.id, str)
        self.assertIsInstance(self.amenity.created_at, datetime)
        self.assertIsInstance(self.amenity.updated_at, datetime)
        self.assertEqual(self.amenity.name, "")

    def test_name(self):
        """Test name attribute."""
        self.amenity.name = "WiFi"
        self.assertEqual(self.amenity.name, "WiFi")

    def test_str(self):
        """Test string representation of Amenity."""
        expected = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str(self.amenity), expected)

    def test_save(self):
        """Test save method updates updated_at."""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(old_updated_at, self.amenity.updated_at)

    def test_to_dict(self):
        """Test to_dict method creates a dictionary with correct attributes."""
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict['__class__'], 'Amenity')
        self.assertEqual(amenity_dict['id'], self.amenity.id)
        self.assertEqual(amenity_dict['created_at'],
                         self.amenity.created_at.isoformat())
        self.assertEqual(amenity_dict['updated_at'],
                         self.amenity.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
