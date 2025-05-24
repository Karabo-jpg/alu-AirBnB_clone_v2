#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime, UTC
import os
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        from models import storage
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        if kwargs:
            valid_attrs = {col.name for col in self.__table__.columns}
            valid_attrs.update({'__class__'})
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
                if key != "__class__" and key not in valid_attrs:
                    raise KeyError(f"Invalid attribute: {key}")
                if key != "__class__":
                    setattr(self, key, value)
        storage.new(self)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now(UTC)
        storage.save()

    def to_dict(self):
        """Converts instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(self.__class__.__name__, self.id, self.__dict__)

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)
