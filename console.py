#!/usr/bin/python3
"""
    This module contains the entry point of the command interpreter
    for this project
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ The command interpreter """

    prompt = "(hbnb) "
    models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def emptyline(self):
        """ Executes when the line is empty """

        pass

    def do_create(self, name):
        """
            Creates a new instance of class name given
            Usage: create <model>
        """

        if not name:
            print("** class name missing **")
        elif name not in HBNBCommand.models:
            print("** class doesn't exist **")
        else:
            cls = HBNBCommand.models[name]
            new = cls()
            new.save()

            print(new.id)

    def do_show(self, line):
        """
            Prints the string representation of an instance based
            on the class name and id
            Usage: show <model> <id>
        """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        model = args[0]
        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        try:
            id = args[1]
        except IndexError:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                print(obj)
                return
        print("** no instance found **")

    def do_destroy(self, line):
        """
            Deletes an instance based on the class name and id
            Usage: destroy <model> <id>
        """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        model = args[0]
        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        try:
            id = args[1]
        except IndexError:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                del obj
                del storage._FileStorage__objects[obj_id]
                storage.save()
                return

        print("** no instance found **")

    def do_all(self, line):
        """
            Prints all string representation of all instances
            based or not on the class name
        """

        all_objs = storage.all()
        all_objs_ptr = []

        if line:
            if line not in HBNBCommand.models:
                print("** class doesn't exist **")
                return

            for obj_id, obj in all_objs.items():
                if obj.__class__.__name__ == line:
                    all_objs_ptr.append(obj.__str__())
        else:
            for obj_id, obj in all_objs.items():
                all_objs_ptr.append(obj.__str__())

        print(all_objs_ptr)

    def do_update(self, line):
        """
            Updates an instance based on class name and id by
            adding or updating attributes
            Usage: update <model> <id> <attribute> "<value>"
        """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        model = args[0]
        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        try:
            id = args[1]
        except IndexError:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        id_exist = False
        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                id_exist = True

        if not id_exist:
            print("** no instance found **")
            return

        try:
            attr_name = args[2]
        except IndexError:
            print("** attribute name missing **")
            return

        attr_vals = []
        try:
            attr_vals.append(args[3])
        except IndexError:
            print("** value missing **")
            return

        if attr_vals[0][-1] != '"':
            i = 4
            while i < len(args):
                attr_vals.append(args[i])
                if args[i][-1] == '"':
                    break

        attr_val = " ".join(attr_vals)

        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                setattr(obj, attr_name, "".join(attr_val.split('"')))
                obj.save()
                break

    def do_quit(self, line):
        """ Quit command to exit the program """

        return True

    def do_EOF(self, line):
        """ end of file """

        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
