#!/usr/bin/python3
"""
    This module contains a class City that inherits from the
    BaseModel class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """ A City class that inherits from BaseModel """

    state_id = ""
    name = ""
