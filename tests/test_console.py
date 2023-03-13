import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class ConsoleTest(unittest.TestCase):
    """ A class to test the console class """

    models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    @classmethod
    def setUpClass(cls):
        """ creates all models to be used for testing """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            cls.base_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            cls.user_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            cls.state_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            cls.city_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            cls.amenity_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            cls.place_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            cls.review_id = f.getvalue()[:-1]

    def setUp(self):
        """ calls before each test """

        all_objs = storage.all()
        rev_key = "Review.{}".format(self.review_id)
        place_key = "Place.{}".format(self.place_id)

        try:
            all_objs[rev_key]
        except KeyError:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("create Review")
                ConsoleTest.review_id = f.getvalue()[:-1]

        try:
            all_objs[place_key]
        except KeyError:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("create Place")
                ConsoleTest.place_id = f.getvalue()[:-1]

    def test_create(self):
        """ test the create command """

        # test create for BaseModel
        with patch("sys.stdout", new=StringIO()) as f:
            # create model and get value printed without '\n'
            HBNBCommand().onecmd("create BaseModel")
            value = f.getvalue()[:-1]

            # test if value is string
            self.assertTrue(type(value) is str)

            all_objs = storage.all()
            obj_key = "BaseModel.{}".format(value)

            # test that key is in storage
            self.assertTrue(obj_key in all_objs)

            # test that id are same
            self.assertEqual(value, all_objs[obj_key].id)

        # test create for User
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            value = f.getvalue()[:-1]
            self.assertTrue(type(value) is str)
            all_objs = storage.all()
            obj_key = "User.{}".format(value)
            self.assertTrue(obj_key in all_objs)
            self.assertEqual(value, all_objs[obj_key].id)

    def test_create_wrong_model(self):
        """ test create with unknown model type """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create MyModel")
            value = f.getvalue()
            self.assertEqual(value, "** class doesn't exist **\n")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Users")
            value = f.getvalue()
            self.assertEqual(value, "** class doesn't exist **\n")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create 1")
            value = f.getvalue()
            self.assertEqual(value, "** class doesn't exist **\n")

    def test_create_no_model(self):
        """ test create ommiting model name """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            value = f.getvalue()
            self.assertEqual(value, "** class name missing **\n")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create  ")
            value = f.getvalue()
            self.assertEqual(value, "** class name missing **\n")

    def test_model_count(self):
        """ test the model.count() command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "2")

        # create new models
        for i in range(3):
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("create User")
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("create Amenity")
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("create City")
        for i in range(10):
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("create Review")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "5")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "11")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "4")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("City.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "4")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "2")

    def test_show(self):
        """ test the show command """

        # test the show command
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State {}".format(self.state_id))
            value = f.getvalue()[:-1]

            # find the new object created in storage
            all_objs = storage.all()
            key = "State.{}".format(self.state_id)
            obj = all_objs[key]

            # test that value is equal to __str__() of obj
            # show command prints the obj using obj.__str__()
            # - so value should be equal to obj.__str__()
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show City {}".format(self.city_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "City.{}".format(self.city_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

    def test_show_wrong_id(self):
        """ test the show comand with wrong id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State 123kkiwq")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show User 123kaeells")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State test")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_show_no_id(self):
        """ test show omitting id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_show_wrong_model(self):
        """ test show with wrong class """

        # test with wrong class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Stat ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show myModel 1123")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show model ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_show_no_model(self):
        """ test show with no model """

        # test with no model
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

    def test_model_show(self):
        """ test the model.show() command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.show(\"{}\")".format(self.state_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "State.{}".format(self.state_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("City.show(\"{}\")".format(self.city_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "City.{}".format(self.city_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

    def test_model_show_wrong_id(self):
        """ test the model.show() comand with wrong id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.show(\"123kkiwq\")")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_model_show_no_id(self):
        """ test the model.show() omitting id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.show()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.show(\"\")")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_model_show_wrong_model(self):
        """ test model.show() with wrong class """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Stat.show()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_destroy(self):
        """ test destroy command """

        # test for review
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Review {}".format(self.review_id))
            value = f.getvalue()
            # doesnt print

    def test_destroy(self):
        """ test destroy command """

        # test for review
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Review {}".format(self.review_id))
            value = f.getvalue()
            # doesnt print
            self.assertEqual(value, "")

        # test that instance doesnt exist for deleted id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Review {}".format(self.review_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        # test for place
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Place {}".format(self.place_id))
            value = f.getvalue()
            # doesnt print
            self.assertEqual(value, "")

        # test that instance doesnt exist for deleted id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Place {}".format(self.place_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_destroy_wrong_id(self):
        """ test the destroy comand with wrong id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State 123kkiwq")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User 123kaeells")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State test")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_destroy_no_id(self):
        """ test destroy omitting id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_destroy_wrong_model(self):
        """ test destroy with wrong class """

        # test with wrong class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Stat ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy myModel 1123")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy model ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_destroy_no_model(self):
        """ test destroy with no model """

        # test with no model
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

    def test_model_destroy(self):
        """ test model.destroy() command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.destroy(\"{}\")"
                                 .format(self.review_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Review {}".format(self.review_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.destroy(\"{}\")".format(self.place_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Place {}".format(self.place_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_model_destroy_wrong_id(self):
        """ test the model.destroy() comand with wrong id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.destroy(\"123kkiwq\")")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.destroy(\"12\")")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_model_destroy_no_id(self):
        """ test model.destroy() omitting id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.destroy()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.destroy(\"\")")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_model_destroy_wrong_model(self):
        """ test model.destroy() with wrong class """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Mymodel.destroy()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_all(self):
        """ test the all command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            value = f.getvalue()[:-1]
            # value will be string that print an array of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = []
            for key in all_objs.keys():
                exp_val.append(all_objs[key].__str__())

            self.assertEqual(value, exp_val.__str__())

    def test_all_model(self):
        """ test all command with model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel ")
            value = f.getvalue()[:-1]
            # value will be string that print an array of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = []
            for key, obj in all_objs.items():
                if obj.__class__.__name__ == "BaseModel":
                    exp_val.append(all_objs[key].__str__())

            self.assertEqual(value, exp_val.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all User ")
            value = f.getvalue()[:-1]
            # value will be string that print an array of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = []
            for key, obj in all_objs.items():
                if obj.__class__.__name__ == "User":
                    exp_val.append(all_objs[key].__str__())

    def test_all2(self):
        """ test all for a model that has no object """

        # check if a model exist and destroy it
        destroy = False
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
            value = f.getvalue()[:-1]

            if value != "** class doesn't exist **":
                destroy = True

        if destroy:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy Review {}"
                                     .format(self.review_id))
                value = f.getvalue()[:-1]

        # test all when model doesnt exist
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
            value = f.getvalue()[:-1]
            self.assertEqual(value, [].__str__())

        # recreate model to prevent failure of other tests
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            value = f.getvalue()[:-1]
            ConsoleTest.review_id = value

    def test_all_wrong_model(self):
        """ test all with wrong class """

        # test with wrong class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Stat ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all myModel 1123")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all model ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_model_all(self):
        """ test model.all() command"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.all()")
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            exp_val = []
            for key, obj in all_objs.items():
                if obj.__class__.__name__ == "BaseModel":
                    exp_val.append(all_objs[key].__str__())

            self.assertEqual(value, exp_val.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.()")
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            exp_val = []
            for key, obj in all_objs.items():
                if obj.__class__.__name__ == "User":
                    exp_val.append(all_objs[key].__str__())

    def test_model_all2(self):
        """ test model.all() for a model that has no object """
        destroy = False
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
            value = f.getvalue()[:-1]

            if value != "** class doesn't exist **":
                destroy = True

        if destroy:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy Review {}"
                                     .format(self.review_id))
                value = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, [].__str__())

        # recreate model to prevent failure of other tests
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            value = f.getvalue()[:-1]
            ConsoleTest.review_id = value

    def test_model_all_wrong_model(self):
        """ test model.all() with wrong class """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("NewModel.all()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_update(self):
        """ test the update command """

        # test update with user
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update User {} first_name \"Samuel\""
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            # update command prints nothing
            self.assertEqual(value, "")

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual("Samuel", obj.first_name)

        # test update with City
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update City {} city_id \"11213ef\""
                    .format(self.city_id))
            value = f.getvalue()[:-1]

            # update command prints nothing
            self.assertEqual(value, "")

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertTrue("city_id" in obj.to_dict())
            self.assertEqual("11213ef", obj.city_id)

    def test_update2(self):
        """ test the update command to update an existing attr """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update User {} first_name \"Samuel John Stones\""
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertEqual("Samuel John Stones", obj.first_name)

        # test update with City
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update City {} city_id \"1e21b\""
                    .format(self.city_id))
            value = f.getvalue()[:-1]

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertEqual("1e21b", obj.city_id)

    def test_update3(self):
        """ test update with more attributes """

        with patch("sys.stdout", new=StringIO()) as f:
            # all other arguments are ignored after first attribute is updated
            command = "update State {} first_name ".format(self.state_id)
            command2 = "\"John John\" last_name \"Emeka\""
            HBNBCommand().onecmd(command + command2)

            # get all objs and find updated obj
            all_objs = storage.all()
            obj_key = "State.{}".format(self.state_id)
            obj = all_objs[obj_key]

            # check that first_name attribute exist and has correct val
            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual(obj.first_name, "John John")

            # check that last_name doesnt exit (was ignored)
            self.assertTrue("last_name" not in obj.to_dict())

    def test_update_no_value(self):
        """ test update when val is ommited """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel {} name"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** value missing **")

    def test_update_no_attribute(self):
        """ test update when attribute missing """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel {}"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** attribute name missing **")

    def test_update_wrong_id(self):
        """ test update wrong id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update Place 110092"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** no instance found **")

    def test_update_no_id(self):
        """ test update with missing id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update Place "
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** instance id missing **")

    def test_update_wrong_model(self):
        """ test update with wrong model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update MyModel "
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

    def test_update_no_model(self):
        """ test update with missing model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update".format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class name missing **")

    def test_model_update(self):
        """ test the model.update() command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", \"first_name\", \"Samuel\")"
                    .format(self.user_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual("Samuel", obj.first_name)

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "City.update(\"{}\", \"city_id\", \"11213ef\")"
                    .format(self.city_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            self.assertTrue("city_id" in obj.to_dict())
            self.assertEqual("11213ef", obj.city_id)

    def test_model_update2(self):
        """ test the model.update() command to update an existing attr """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", \"first_name\", \"Samuel Stones\")"
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertEqual("Samuel Stones", obj.first_name)

    def test_model_update3(self):
        """ test model.update() with more attributes """

        with patch("sys.stdout", new=StringIO()) as f:
            command = "State.update(\"{}\", \"first_name\", ".format(
                                                            self.state_id)
            command2 = "\"John John\", \"last_name\", \"Emeka\")"
            HBNBCommand().onecmd(command + command2)

            all_objs = storage.all()
            obj_key = "State.{}".format(self.state_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual(obj.first_name, "John John")

            self.assertTrue("last_name" not in obj.to_dict())

    def test_model_update_no_value(self):
        """ test model.update() when val is ommited """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(\"{}\", \"name\")"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** value missing **")

    def test_model_update_no_attribute(self):
        """ test model.update() when attribute missing """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(\"{}\")"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** attribute name missing **")

    def test_model_update_wrong_id(self):
        """ test model.update() wrong id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.update(\"110092\")"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** no instance found **")

    def test_model_update_no_id(self):
        """ test model.update() with missing id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.update()"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** instance id missing **")

    def test_model_update_wrong_model(self):
        """ test model.update() with wrong model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("MyModel.update()"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

    def test_model_update_dict1(self):
        """ test the model.update() command with dict"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", {{'first_name': 'John'}})"
                    .format(self.user_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual("John", obj.first_name)

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "City.update(\"{}\", {{'city_id': '11213'}})"
                    .format(self.city_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            self.assertTrue("city_id" in obj.to_dict())
            self.assertEqual("11213", obj.city_id)

    def test_model_update_dict2(self):
        """ test the model.update() command to update an existing attr """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", {{\"first_name\": 'Samuel Stones'}})"
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertEqual("Samuel Stones", obj.first_name)

    def test_model_update_dict3(self):
        """ test model.update() with more attributes """

        with patch("sys.stdout", new=StringIO()) as f:
            command = "User.update(\"{}\", {{'first_name': ".format(
                                                            self.user_id)
            command2 = "\"John John\", \"last_name\": 'Emeka', 'age': 89})"
            HBNBCommand().onecmd(command + command2)

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual(obj.first_name, "John John")

            self.assertTrue("last_name" in obj.to_dict())
            self.assertEqual(obj.last_name, "Emeka")

            self.assertTrue("age" in obj.to_dict())
            self.assertEqual(obj.age, 89)

    def test_model_update_dict_wrong_id(self):
        """ test the model.update() command with wrong id"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"112345\", {'first_name': 'John'})")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_model_update_dict_no_id(self):
        """ test the model.update() command with no id"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update({'first_name': 'John'})")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_model_update_dict_wrong_model(self):
        """ test model.update() with wrong model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("MyModel.update()"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

    def test_quit(self):
        """ test the quit command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            value = f.getvalue()

            self.assertEqual(value, "")

    def test_invalid_args(self):
        """ test some invalid args """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("hello Model")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: hello Model")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Model.create()")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: Model.create()")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Model.hide()")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: Model.hide()")

    def test_invalid_args2(self):
        """ test some invalid args """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Model")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: Model")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.update(")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: User.update(")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("how()")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: how()")
