#!/usr/bin/python3
"""Defines the FileStorage class for file-based storage."""
import json


class FileStorage:
    """Manages file-based storage for the AirBnB project."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary of objects."""
        return self.__objects

    def new(self, obj):
        """Add a new object to the storage dictionary."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize objects to the JSON file."""
        serialized = {
            key: obj.to_dict() for key, obj in self.__objects.items()
        }
        with open(self.__file_path, 'w') as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserialize the JSON file to objects."""
        from models.base_model import BaseModel
        from models.state import State
        from models.city import City
        classes = {
            "BaseModel": BaseModel,
            "State": State,
            "City": City
        }
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    cls_name = value["__class__"]
                    if cls_name in classes:
                        self.__objects[key] = classes[cls_name](**value)
        except FileNotFoundError:
            pass
