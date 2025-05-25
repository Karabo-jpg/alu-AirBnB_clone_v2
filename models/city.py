#!/usr/bin/python3
"""This module defines the City class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """This class defines a city by various attributes."""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False, default="")
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False,
                      default="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    pass
