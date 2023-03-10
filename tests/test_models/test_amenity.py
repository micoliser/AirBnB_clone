import unittest
import os
from datetime import datetime
from models import storage
from models.amenity import Amenity


class AmenityTest(unittest.TestCase):
    """ A class to test the Amenity class """

    def test_amenity1(self):
        """ Test amenity """

        a1 = Amenity()

        # test default types
        self.assertEqual(len(a1.id), 36)
        self.assertTrue(type(a1.created_at) is datetime)
        self.assertTrue(type(a1.updated_at) is datetime)
        self.assertTrue(type(a1.name) is str)
        self.assertTrue(a1.created_at == a1.updated_at)

    def test_amenity2(self):
        """ Test amenity """

        a1 = Amenity()

        # test default values
        self.assertEqual(a1.name, "")

    def test_amenity3(self):
        """ Test amenity model """

        a1 = Amenity()
        a1.name = "amenity1"

        self.assertTrue(type(a1.id) is str)
        self.assertEqual(a1.name, "amenity1")

    def test_amenity_args(self):
        """ Test amenity model with args """

        a1 = Amenity(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(a1.id is not None)
        self.assertTrue(a1.id != 1)
        self.assertTrue(a1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(a1.created_at is not None)
        self.assertTrue(a1.created_at != 1)
        self.assertTrue(a1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(a1.updated_at is not None)
        self.assertTrue(a1.updated_at != 1)
        self.assertTrue(a1.updated_at != 3)

    def test_amenity_kwargs(self):
        """ test amenity with kwargs """

        a1 = Amenity()
        a1.name = "amenity1"
        a1_dict = a1.to_dict()
        a2 = Amenity(**a1_dict)

        self.assertEqual(a1.id, a2.id)
        self.assertEqual(a1.created_at, a2.created_at)
        self.assertEqual(a1.updated_at, a2.updated_at)
        self.assertEqual(a1.name, a2.name)
        self.assertTrue(a1 is not a2)

    def test_amenity_str(self):
        """ test __str__ method of amenity """

        a1 = Amenity()
        out_str = "[{}] ({}) {}".format(
                 a1.__class__.__name__, a1.id, a1.__dict__
                )

        self.assertEqual(a1.__str__(), out_str)

    def test_amenity_save(self):
        """ test the save method of amenity """

        a1 = Amenity()

        # test that created_at and updated_at attributes are same
        self.assertEqual(a1.created_at, a1.updated_at)

        a1.save()  # saves a1 to file. Now updated_at will be different
        self.assertTrue(a1.created_at != a1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

        os.remove("file.json")

    def test_amenity_save_args(self):
        """ test the save method with args """

        a1 = Amenity()

        with self.assertRaises(TypeError):
            a1.save(1, 2)

    def test_amenity_to_dict1(self):
        """ test the to_dict method """

        a1 = Amenity()
        a1.name = "amenity1"
        a1_dict = a1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id", "name"]

        self.assertTrue(type(a1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in a1_dict)

    def test_amenity_to_dict2(self):
        """ test the to_dict method """

        a1 = Amenity()
        a1.name = "amenity1"
        a1_dict = a1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(a1_dict["updated_at"] is str))
        self.assertTrue(type(a1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(a1_dict["__class__"], "Amenity")

        self.assertEqual(a1.name, a1_dict["name"])

    def test_amenity_to_dict_args(self):
        """ test the to_dict method with args """

        a1 = Amenity()

        with self.assertRaises(TypeError):
            a1.to_dict("h")
