#!/usr/bin/python3
"""Tests for State class."""
import unittest
import os
from models.state import State
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage


class TestState(unittest.TestCase):
    """Test cases for the State class."""

    def setUp(self):
        """Set up test environment."""
        self.state = State()

    def test_init(self):
        """Test initialization of State."""
        self.assertEqual(self.state.name, "")
        self.assertTrue(hasattr(self.state, 'id'))
        self.assertTrue(hasattr(self.state, 'created_at'))

    def test_save(self):
        """Test the save method."""
        old_updated_at = self.state.updated_at
        self.state.save()
        self.assertNotEqual(old_updated_at, self.state.updated_at)

    def test_to_dict(self):
        """Test the to_dict method."""
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertEqual(state_dict['created_at'],
                         self.state.created_at.isoformat())
        self.assertEqual(state_dict['updated_at'],
                         self.state.updated_at.isoformat())

    def test_str(self):
        """Test the __str__ method."""
        expected = "[State] ({}) {}".format(self.state.id, self.state.__dict__)
        self.assertEqual(str(self.state), expected)

    def test_name_attribute(self):
        """Test the name attribute."""
        self.state.name = "California"
        self.assertEqual(self.state.name, "California")


if __name__ == '__main__':
    unittest.main()
