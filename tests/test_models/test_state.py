#!/usr/bin/python3
"""Tests for State class."""
import unittest
from models.state import State
from datetime import datetime
from models import storage


class TestState(unittest.TestCase):
    """Test cases for the State class."""

    def setUp(self):
        """Set up before each test."""
        self.state = State()

    def test_init(self):
        """Test initialization of State."""
        self.assertIsInstance(self.state.id, str)
        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsInstance(self.state.updated_at, datetime)
        self.assertEqual(self.state.name, "")

    def test_name(self):
        """Test name attribute."""
        self.state.name = "California"
        self.assertEqual(self.state.name, "California")

    def test_str(self):
        """Test string representation of State."""
        expected = f"[State] ({self.state.id}) {self.state.__dict__}"
        self.assertEqual(str(self.state), expected)

    def test_save(self):
        """Test save method updates updated_at."""
        old_updated_at = self.state.updated_at
        self.state.save()
        self.assertNotEqual(old_updated_at, self.state.updated_at)

    def test_to_dict(self):
        """Test to_dict method creates a dictionary with correct attributes."""
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertEqual(state_dict['id'], self.state.id)
        self.assertEqual(state_dict['created_at'],
                         self.state.created_at.isoformat())
        self.assertEqual(state_dict['updated_at'],
                         self.state.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
