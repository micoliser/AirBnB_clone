#!/usr/bin/python3
"""
    This module contains the entry point of the command interpreter
    for this project
"""
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """ The command interpreter """

    prompt = "(hbnb) "
    models = {"BaseModel": BaseModel}

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
            if id == obj.id:
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
            if obj.id == id:
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
            Usage: update <model> <id> <attribute> <value>
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
            if obj.id == id:
                id_exist = True

        if not id_exist:
            print("** no instance found **")
            return

        try:
            attr_name = args[2]
        except IndexError:
            print("** attribute name missing **")
            return

        try:
            attr_val = args[3]
        except IndexError:
            print("** value missing **")
            return

        for obj_id, obj in all_objs.items():
            if obj.id == id:
                setattr(obj, attr_name, attr_val)
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
