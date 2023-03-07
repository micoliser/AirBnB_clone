#!/usr/bin/python3
"""
    This module contains a FileSorage class that serializes instnaces
    to a json file and deserializes json files to instances
"""
import json


class FileStorage:
    """ A class that serializes and deserializes instances to json """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dict __objects """

        return FileStorage.__objects

    def new(self, obj):
        """ sets a new obj in __objects """

        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to json file """

        json_dict = {key: val.to_dict()
                     for key, val in FileStorage.__objects.items()}

        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(json_dict))

    def reload(self):
        """ deserializes json file to __objects """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        model_dict = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

        try:
            with open(FileStorage.__file_path, "r") as f:
                json_dict = json.loads(f.read())
                FileStorage.__objects = {}

                for key, val in json_dict.items():
                    if val["__class__"] in model_dict:
                        cls = model_dict[val["__class__"]]
                        obj = cls(**val)
                        FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass
