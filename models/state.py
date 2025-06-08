#!/usr/bin/python3
"""
State class for the AirBnB project
"""
from models.base_model import BaseModel
from models.city import City
from os import getenv

class State(BaseModel):
    """State class representing a state entity"""

    def __init__(self, *args, **kwargs):
        """Initialize a new State instance"""
        super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """Getter method to return the list of City objects linked to the State."""
        from models import storage
        if getenv("HBNB_TYPE_STORAGE") != "db":
            cities_list = []
            all_cities = storage.all(City).values()
            for city in all_cities:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
        return []
