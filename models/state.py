#!/usr/bin/python3
"""This module defines the State class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """This class defines a state by various attributes."""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False, default="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    pass
