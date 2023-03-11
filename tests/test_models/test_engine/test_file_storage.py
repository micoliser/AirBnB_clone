import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class FileStorageTest(unittest.TestCase):
    """ Test the FileStorage class """

    s_test = FileStorage()
    s_objs = s_test._FileStorage__objects
    s_file = s_test._FileStorage__file_path

    @classmethod
    def setUpClass(cls):
        """ class before the tests """

        objs = cls.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del cls.s_test._FileStorage__objects[key]

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_storage1(self):
        """ test file storage """

        # test default types
        self.assertTrue(type(self.s_file) is str)
        self.assertTrue(type(self.s_objs) is dict)

    def test_storage2(self):
        """ test file storage """

        # test default values
        self.assertEqual(self.s_file, "file.json")
        self.assertEqual(self.s_objs, {})

    def test_storage_new(self):
        """ Test the new method """

        # create one instance each of all model to test with
        # all models call the new() function of the FileStrorage class
        # - and saves all objects to FileStorage.__objects
        b1 = BaseModel()
        u1 = User()
        s1 = State()
        c1 = City()
        a1 = Amenity()
        p1 = Place()
        r1 = Review()
        objs = [b1, u1, s1, c1, a1, p1, r1]

        # test that len of __objects is 7 (1 key each for each model created)
        self.assertEqual(len(self.s_objs), 7)

        # test that each obj in __objects is same as each model
        # - and each key is in the form of <modelclassname>.<modelid>
        i = 0
        for key, val in self.s_objs.items():
            obj_key = "{}.{}".format(objs[i].__class__.__name__, objs[i].id)
            self.assertEqual(obj_key, key)
            self.assertTrue(val is objs[i])
            i += 1

    def test_storage_new_more_args(self):
        """ Test the new method with more args """

        with self.assertRaises(TypeError):
            self.s_test.new("b1", "u1")

    def test_storage_new_less_args(self):
        """ Test the new method with less args """

        with self.assertRaises(TypeError):
            self.s_test.new()

    def test_storage_all(self):
        """ Test the all method """

        all_objs = self.s_test.all()

        self.assertTrue(type(all_objs) is dict)

        for key, val in all_objs.items():
            self.assertTrue(key in self.s_objs)
            self.assertEqual(val, self.s_objs[key])

        self.assertTrue(all_objs is self.s_objs)

    def test_storage_all_args(self):
        """ test the all method with args """

        with self.assertRaises(TypeError):
            all_objs = self.s_test.all("12")

    def test_storage_save_and_reload(self):
        """ test the save method and reload """

        # test that file.json does not exist before saving
        self.assertFalse(os.path.exists(self.s_file))

        # call the save method on storage
        self.s_test.save()

        # check that file.json exists
        self.assertTrue(os.path.exists(self.s_file))
        self.assertTrue(os.path.isfile(self.s_file))

        # delete all objects from __objects so its empty
        obj_dict = self.s_objs.copy()
        for key, val in obj_dict.items():
            del self.s_objs[key]

        # check that everything is deleted
        self.assertEqual(len(self.s_objs), 0)
        self.assertEqual(len(self.s_test._FileStorage__objects), 0)

        # reload objects from file
        self.s_test.reload()
        FileStorageTest.s_objs = self.s_test._FileStorage__objects

        # check that objects has been reloaded
        self.assertEqual(len(self.s_objs), 7)
        self.assertEqual(len(self.s_test._FileStorage__objects), 7)
        models = [BaseModel, User, State, City, Amenity, Place, Review]
        i = 0
        for key, val in self.s_objs.items():
            self.assertTrue(type(val) is models[i])
            i += 1

    def test_storage_save_args(self):
        """ test the save method with args """

        with self.assertRaises(TypeError):
            self.s_test.save("hey")

    def test_storage_reload_args(self):
        """ test the reload method with args """

        with self.assertRaises(TypeError):
            self.s_test.save(12)

    @classmethod
    def tearDownClass(cls):
        """ calls after the tests """

        objs = cls.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del cls.s_test._FileStorage__objects[key]

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
