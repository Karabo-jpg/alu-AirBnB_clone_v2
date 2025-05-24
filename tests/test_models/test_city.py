#!/usr/bin/python3
"""Tests for City class."""
import unittest
from models.city import City


class TestCity(unittest.TestCase):
    """Test cases for the City class."""

    def setUp(self):
        """Set up test environment."""
        self.city = City()

    def test_init(self):
        """Test initialization of City."""
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")
