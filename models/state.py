#!/usr/bin/python3
"""This module defines the State class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This class defines a state by various attributes."""
    __tablename__ = 'states'

    name = Column(String(128), nullable=False, default="")
    cities = relationship("City", backref="state", cascade="all, delete-orphan")


if __name__ == "__main__":
    pass
