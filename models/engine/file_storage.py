#!/usr/bin/python3
"""This module defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


class FileStorage:
    """This class serializes instances to a JSON file and deserializes back."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of all objects or objects of a specific class.
        
        Args:
            cls (type, optional): If provided, returns only objects of this class.
                                 If None, returns all objects.
        Returns:
            dict: A dictionary of objects filtered by class if specified.
        """
        if cls is None:
            return self.__objects
        filtered = {}
        for key, value in self.__objects.items():
            if isinstance(value, cls):
                filtered[key] = value
        return filtered

    def new(self, obj):
        """Add a new object to __objects."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file."""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(serialized_objects, f)

    def reload(self):
        """Deserialize the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name = value["__class__"]
                    if class_name in classes:
                        self.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an object from __objects if it exists.
        
        Args:
            obj: The object to delete. If None, do nothing.
            
        This method removes an object from the storage if it exists.
        If obj is None, the method does nothing.
        After deletion, the storage is automatically saved.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()


if __name__ == "__main__":
    pass
