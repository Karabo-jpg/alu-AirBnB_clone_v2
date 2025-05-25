#!/usr/bin/python3
"""This module defines the Amenity class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class Amenity(BaseModel, Base):
    """This class defines an amenity by various attributes."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False, default="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    pass
