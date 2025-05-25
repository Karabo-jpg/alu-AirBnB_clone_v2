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
        self.storage._FileStorage__objects.clear()
        if os.path.exists("file.json"):
            os.remove("file.json")
        self.storage.save()  # Save an empty state
        self.storage.reload()  # Reload to ensure consistency

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
        self.console.onecmd('create City state_id="123" name="San_Francisco"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_user_in_file(self):
        """Test that creating a User adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create User email="user@example.com" password="pwd"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_place_in_file(self):
        """Test that creating a Place adds it to the JSON file."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create Place city_id="123" user_id="456" name="Cozy_Cabin"')
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
        self.console.onecmd('create Review place_id="123" user_id="456" text="Great_stay!"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_delete_state_in_file(self):
        """Test that deleting a State removes it from the JSON file."""
        self.console.onecmd('create State name="Nevada"')
        state_id = list(self.storage.all().values())[0].id
        initial_count = len(self.storage.all())
        self.console.onecmd(f'destroy State {state_id}')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count - 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_delete_city_in_file(self):
        """Test that deleting a City removes it from the JSON file."""
        self.console.onecmd('create City state_id="123" name="Las_Vegas"')
        city_id = list(self.storage.all().values())[0].id
        initial_count = len(self.storage.all())
        self.console.onecmd(f'destroy City {city_id}')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count - 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_state_in_file(self):
        """Test that updating a State modifies the JSON file."""
        self.console.onecmd('create State name="Arizona"')
        state_id = list(self.storage.all().values())[0].id
        self.console.onecmd(f'update State {state_id} name "New_Arizona"')
        self.storage.reload()
        for obj in self.storage.all().values():
            if obj.__class__.__name__ == "State" and obj.id == state_id:
                self.assertEqual(obj.name, "New_Arizona")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_user_in_file(self):
        """Test that updating a User modifies the JSON file."""
        self.console.onecmd('create User email="user@example.com" password="pwd"')
        user_id = list(self.storage.all().values())[0].id
        self.console.onecmd(f'update User {user_id} first_name "John"')
        self.storage.reload()
        for obj in self.storage.all().values():
            if obj.__class__.__name__ == "User" and obj.id == user_id:
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
        for obj in state_objects.values():
            self.assertEqual(obj.__class__.__name__, "State")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_reload_empty_file(self):
        """Test reload with an empty file."""
        with open("file.json", "w") as f:
            f.write("{}")
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_invalid_state(self):
        """Test creating a State with invalid input."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create State name=Invalid\\ Space')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_nonexistent_object(self):
        """Test updating a non-existent object."""
        initial_count = len(self.storage.all())
        self.console.onecmd('update State "nonexistent" name "Invalid"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_delete_nonexistent_object(self):
        """Test deleting a non-existent object."""
        initial_count = len(self.storage.all())
        self.console.onecmd('destroy State "nonexistent"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_multiple_states(self):
        """Test creating multiple States."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create State name="California"')
        self.console.onecmd('create State name="Nevada"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 2)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_save_without_changes(self):
        """Test saving without changes doesn't affect file."""
        self.console.onecmd('create State name="Oregon"')
        self.storage.reload()
        initial_content = ""
        with open("file.json", "r") as f:
            initial_content = f.read()
        self.storage.save()
        new_content = ""
        with open("file.json", "r") as f:
            new_content = f.read()
        self.assertEqual(new_content, initial_content)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_reload_after_delete(self):
        """Test reload after deleting an object."""
        self.console.onecmd('create State name="Washington"')
        state_id = list(self.storage.all().values())[0].id
        self.console.onecmd(f'destroy State {state_id}')
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_with_special_characters(self):
        """Test creating an object with special characters in attributes."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create State name="New_York_!@#"')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_create_with_numeric_values(self):
        """Test creating a Place with numeric attributes."""
        initial_count = len(self.storage.all())
        self.console.onecmd('create Place city_id="123" user_id="456" name="Villa" number_rooms=3')
        self.storage.reload()
        new_count = len(self.storage.all())
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_with_special_characters(self):
        """Test updating an object with special characters."""
        self.console.onecmd('create State name="Arizona"')
        state_id = list(self.storage.all().values())[0].id
        self.console.onecmd(f'update State {state_id} name "Arizona_!@#"')
        self.storage.reload()
        for obj in self.storage.all().values():
            if obj.__class__.__name__ == "State" and obj.id == state_id:
                self.assertEqual(obj.name, "Arizona_!@#")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_update_numeric_attribute(self):
        """Test updating a numeric attribute."""
        self.console.onecmd('create Place city_id="123" user_id="456" name="Villa"')
        place_id = list(self.storage.all().values())[0].id
        self.console.onecmd(f'update Place {place_id} number_rooms 5')
        self.storage.reload()
        for obj in self.storage.all().values():
            if obj.__class__.__name__ == "Place" and obj.id == place_id:
                self.assertEqual(obj.number_rooms, 5)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_all_empty_storage(self):
        """Test all() on empty storage."""
        self.assertEqual(len(self.storage.all()), 0)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Not using file storage")
    def test_reload_corrupted_file(self):
        """Test reload with a corrupted JSON file."""
        with open("file.json", "w") as f:
            f.write("{invalid_json")
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)


if __name__ == '__main__':
    unittest.main()
