#!/usr/bin/python3
"""This module defines the BaseModel class."""
from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """This class defines all common attributes/methods for other classes."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value if value is not None else "")
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance."""
        dict_copy = self.__dict__.copy()
        if "_sa_instance_state" in dict_copy:
            del dict_copy["_sa_instance_state"]
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        return dict_copy

if __name__ == "__main__":
    pass
