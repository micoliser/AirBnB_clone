#!/usr/bin/python3
"""
    This module contains a class User that inherits from the
    BaseModel class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """ A user class that inherits from BaseModel """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
