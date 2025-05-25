#!/usr/bin/python3
"""This module defines the Review class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """This class defines a review by various attributes."""
    __tablename__ = 'reviews'

    place_id = Column(String(60), ForeignKey('places.id'), nullable=False, default="")
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False, default="")
    text = Column(String(1024), nullable=True, default="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    pass
