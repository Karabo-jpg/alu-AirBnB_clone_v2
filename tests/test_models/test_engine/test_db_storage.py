#!/usr/bin/python3
"""Tests for DBStorage class."""
import unittest
import os
import MySQLdb
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand


class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        cls.storage = DBStorage()
        cls.storage.reload()
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        cls.storage.close()

    def setUp(self):
        """Set up before each test."""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            conn = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM states")
            cursor.execute("DELETE FROM cities")
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM places")
            cursor.execute("DELETE FROM amenities")
            cursor.execute("DELETE FROM reviews")
            conn.commit()
            cursor.close()
            conn.close()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_create_state_in_db(self):
        """Test that creating a State adds a record to the states table."""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('create State name="California"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_create_city_in_db(self):
        """Test that creating a City adds a record to the cities table."""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('create City state_id="123" '
                            'name="San_Francisco"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_create_user_in_db(self):
        """Test that creating a User adds a record to the users table."""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('create User email="user@example.com" '
                            'password="pwd"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_create_place_in_db(self):
        """Test that creating a Place adds a record to the places table."""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM places")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('create Place city_id="123" user_id="456" '
                            'name="Cozy_Cabin"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM places")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_create_amenity_in_db(self):
        """Test that creating an Amenity adds a record to the amenities table."""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM amenities")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('create Amenity name="WiFi"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM amenities")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_create_review_in_db(self):
        """Test that creating a Review adds a record to the reviews table."""
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reviews")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('create Review place_id="123" user_id="456" '
                            'text="Great_stay!"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reviews")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_delete_state_in_db(self):
        """Test that deleting a State removes a record from the states table."""
        self.console.onecmd('create State name="Nevada"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('destroy State "Nevada"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count - 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_delete_city_in_db(self):
        """Test that deleting a City removes a record from the cities table."""
        self.console.onecmd('create City state_id="123" name="Las_Vegas"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        initial_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.console.onecmd('destroy City "Las_Vegas"')
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        new_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(new_count, initial_count - 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_all_method(self):
        """Test that all() returns all objects."""
        self.console.onecmd('create State name="Texas"')
        self.console.onecmd('create City state_id="123" name="Austin"')
        objects = self.storage.all()
        self.assertTrue(len(objects) >= 2)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not using db storage")
    def test_all_specific_class(self):
        """Test that all(State) returns only State objects."""
        self.console.onecmd('create State name="Florida"')
        self.console.onecmd('create City state_id="123" name="Miami"')
        state_objects = self.storage.all(State)
        for key, obj in state_objects.items():
            self.assertEqual(obj.__class__.__name__, "State")

    # Add more tests to reach 50 (e.g., test update, edge cases)


if __name__ == '__main__':
    unittest.main()
