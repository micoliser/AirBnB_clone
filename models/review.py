#!/usr/bin/python3
"""
    This module contains a class Review that inherits from the
    BaseModel class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """ A Review class that inherits from BaseModel """

    place_id = ""
    user_id = ""
    text = ""
