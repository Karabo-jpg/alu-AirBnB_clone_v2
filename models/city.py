#!/usr/bin/python3
"""Defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a City in the AirBnB project."""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new City instance."""
        super().__init__(*args, **kwargs)
