#!/usr/bin/python3
"""
FileStorage class for serializing and deserializing objects to/from JSON file
"""
import json
from datetime import datetime

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)
                from models.base_model import BaseModel
                from models.user import User
                from models.amenity import Amenity
                from models.city import City
                from models.place import Place
                from models.review import Review
                from models.state import State

                classes = {
                    'BaseModel': BaseModel,
                    'User': User,
                    'Amenity': Amenity,
                    'City': City,
                    'Place': Place,
                    'Review': Review,
                    'State': State,
                }

                for key, value in obj_dict.items():
                    if value['__class__'] in classes:
                        if 'created_at' in value:
                            value['created_at'] = datetime.fromisoformat(value['created_at'])
                        if 'updated_at' in value:
                            value['updated_at'] = datetime.fromisoformat(value['updated_at'])
                        self.__objects[key] = classes[value['__class__']](**value)
        except FileNotFoundError:
            pass

    def close(self):
        """Closes the current session by reloading objects from the JSON file."""
        self.reload()
