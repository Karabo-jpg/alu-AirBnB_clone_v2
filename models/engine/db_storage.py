#!/usr/bin/python3
"""This module defines a class to manage database storage for AirBnB clone."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """This class manages storage of AirBnB models in a MySQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database storage engine."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a given class or all classes if cls is None."""
        classes = [User, State, City, Amenity, Place, Review]
        objects = {}

        if cls:
            for obj in self.__session.query(cls).all():
                objects[f"{cls.__name__}.{obj.id}"] = obj
        else:
            for class_type in classes:
                for obj in self.__session.query(class_type).all():
                    objects[f"{class_type.__name__}.{obj.id}"] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the current session."""
        self.__session.remove()
