#!/usr/bin/python3
"""Test module for the console."""
import unittest
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """Test cases for the HBNBCommand class."""

    def setUp(self):
        """Set up test environment."""
        self.console = HBNBCommand()

    def test_quit(self):
        """Test the quit command."""
        self.assertTrue(self.console.do_quit(""))

    def test_EOF(self):
        """Test the EOF command."""
        self.assertTrue(self.console.do_EOF(""))

    def test_emptyline(self):
        """Test empty line behavior."""
        self.assertIsNone(self.console.emptyline())


if __name__ == '__main__':
    unittest.main()
