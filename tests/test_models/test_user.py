#!/usr/bin/python3
"""Tests for User class."""
import unittest
from models.user import User
from datetime import datetime


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    def setUp(self):
        """Set up before each test."""
        self.user = User()

    def test_init(self):
        """Test initialization of User."""
        self.assertIsInstance(self.user.id, str)
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_email(self):
        """Test email attribute."""
        self.user.email = "test@example.com"
        self.assertEqual(self.user.email, "test@example.com")

    def test_password(self):
        """Test password attribute."""
        self.user.password = "password123"
        self.assertEqual(self.user.password, "password123")

    def test_first_name(self):
        """Test first_name attribute."""
        self.user.first_name = "John"
        self.assertEqual(self.user.first_name, "John")

    def test_last_name(self):
        """Test last_name attribute."""
        self.user.last_name = "Doe"
        self.assertEqual(self.user.last_name, "Doe")

    def test_str(self):
        """Test string representation of User."""
        expected = f"[User] ({self.user.id}) {self.user.__dict__}"
        self.assertEqual(str(self.user), expected)

    def test_save(self):
        """Test save method updates updated_at."""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(old_updated_at, self.user.updated_at)

    def test_to_dict(self):
        """Test to_dict method creates a dictionary with correct attributes."""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['id'], self.user.id)
        self.assertEqual(user_dict['created_at'],
                         self.user.created_at.isoformat())
        self.assertEqual(user_dict['updated_at'],
                         self.user.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
