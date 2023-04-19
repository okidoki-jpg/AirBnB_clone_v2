#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class Amenity(BaseModel):
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize Amenity Instance
        """
        super().__init__(*args, **kwargs)
