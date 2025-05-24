#!/usr/bin/python3
"""Defines the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a State in the AirBnB project."""

    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new State instance."""
        super().__init__(*args, **kwargs)
