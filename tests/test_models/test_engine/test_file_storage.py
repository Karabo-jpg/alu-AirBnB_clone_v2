#!/usr/bin/python3
"""Tests for FileStorage class."""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        cls.storage = FileStorage()
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        cls.storage._FileStorage__objects = {}
        if os.path.exists("file.json"):
            os.remove("file.json")

    def setUp(self):
        """Set up before each test."""
        self.storage._FileStorage__objects = {}
        self.storage.save()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_state_in_file(self):
        """Test that creating a State adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create State name="California"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_city_in_file(self):
        """Test that creating a City adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create City state_id="123" '
                            'name="San_Francisco"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_user_in_file(self):
        """Test that creating a User adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create User email="user@example.com" '
                            'password="pwd"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_place_in_file(self):
        """Test that creating a Place adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create Place city_id="123" user_id="456" '
                            'name="Cozy_Cabin"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_amenity_in_file(self):
        """Test that creating an Amenity adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create Amenity name="WiFi"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_review_in_file(self):
        """Test that creating a Review adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create Review place_id="123" user_id="456" '
                            'text="Great_stay!"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_delete_state_in_file(self):
        """Test that deleting a State removes it from the JSON file."""
        self.console.onecmd('create State name="Nevada"')
        initial_count = len(self.storage.all())
        self.console.onecmd('destroy State "Nevada"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count - 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_delete_city_in_file(self):
        """Test that deleting a City removes it from the JSON file."""
        self.console.onecmd('create City state_id="123" name="Las_Vegas"')
        initial_count = len(self.storage.all())
        self.console.onecmd('destroy City "Las_Vegas"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count - 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_state_in_file(self):
        """Test that updating a State modifies the JSON file."""
        self.console.onecmd('create State name="Arizona"')
        self.console.onecmd('update State "Arizona" name "New_Arizona"')
        self.storage.reload()
        for obj in self.storage.all().values():
            if obj.__class__.__name__ == "State":
                self.assertEqual(obj.name, "New_Arizona")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_user_in_file(self):
        """Test that updating a User modifies the JSON file."""
        self.console.onecmd('create User email="user@example.com" '
                            'password="pwd"')
        self.console.onecmd('update User "user@example.com" '
                            'first_name "John"')
        self.storage.reload()
        for obj in self.storage.all().values():
            if obj.__class__.__name__ == "User":
                self.assertEqual(obj.first_name, "John")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_all_method(self):
        """Test that all() returns all objects."""
        self.console.onecmd('create State name="Texas"')
        self.console.onecmd('create City state_id="123" name="Austin"')
        self.storage.reload()
        objects = self.storage.all()
        self.assertTrue(len(objects) >= 2)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_all_specific_class(self):
        """Test that all(State) returns only State objects."""
        self.console.onecmd('create State name="Florida"')
        self.console.onecmd('create City state_id="123" name="Miami"')
        self.storage.reload()
        state_objects = self.storage.all(State)
        for key, obj in state_objects.items():
            self.assertEqual(obj.__class__.__name__, "State")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_reload_empty_file(self):
        """Test reload with an empty file."""
        with open("file.json", "w") as f:
            f.write("{}")
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

    # Add more tests to reach 50 (e.g., edge cases, invalid inputs)


if __name__ == '__main__':
    unittest.main()
