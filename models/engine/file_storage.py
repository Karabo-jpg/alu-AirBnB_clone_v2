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
        """Return a dictionary of all objects or objects of a specific class."""
        if cls is None:
            return self.__objects
        filtered = {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}
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
        from models import storage
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name = value["__class__"]
                    if class_name in classes:
                        self.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    pass
