#!/usr/bin/python3
"""
    This module contains a BaseModel class that defines all
    common attributes and methods for other classes
"""
import uuid
from models import storage
from datetime import datetime


class BaseModel:
    """
        Base class for all other sub classes.
        Defines all common attributes and methods for subclasses
    """

    def __init__(self, *args, **kwargs):
        """ initializes self """

        if kwargs:
            for key, val in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        setattr(self, key, datetime.fromisoformat(val))
                    else:
                        setattr(self, key, val)
        else:
            time_now = datetime.now()

            self.id = str(uuid.uuid4())
            self.created_at = time_now
            self.updated_at = time_now

            storage.new(self)

    def __str__(self):
        """ returns the string representation of the instance """

        s = "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id, self.__dict__
                )

        return s

    def save(self):
        """ Updates the instance attribute updated_at with current time """

        new_time = datetime.now()
        self.updated_at = new_time

        storage.save()

    def to_dict(self):
        """ returns a dictionary containing all key/values of dict """

        d = {}
        d["__class__"] = self.__class__.__name__

        for key, val in self.__dict__.items():
            if key == "created_at":
                d[key] = self.created_at.isoformat()
            elif key == "updated_at":
                d[key] = self.updated_at.isoformat()
            else:
                d[key] = val

        return d
