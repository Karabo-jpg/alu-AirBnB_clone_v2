#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os

classes = {
    'User': User, 'Place': Place, 'State': State,
    'City': City, 'Amenity': Amenity, 'Review': Review
}

class DBStorage:
    """This class manages storage of hbnb models in a MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage with MySQL database connection"""
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')
        self.__engine = create_engine(
            f'mysql+pymysql://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}'
            f'@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}',
            pool_pre_ping=True
        )
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)
        self.reload()

    def all(self, cls=None):
        """Query all objects of a class or all classes"""
        objects = {}
        if cls:
            if cls in classes.values():
                for obj in self.__session.query(cls).all():
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for model_class in classes.values():
                for obj in self.__session.query(model_class).all():
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def new(self, obj):
        """Add object to the current session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the current session"""
        self.__session.remove()
