import unittest
from datetime import datetime
from models.base_model import BaseModel


class BaseModelTest(unittest.TestCase):
    """ A class to test the BaseModel class """

    def test_base1(self):
        """ Test base model """

        b1 = BaseModel()

        self.assertEqual(len(b1.id), 36)
        self.assertTrue(type(b1.created_at) == datetime)
        self.assertTrue(type(b1.updated_at) == datetime)
        self.assertTrue(b1.created_at == b1.updated_at)

    def test_base2(self):
        """ Test base model """

        b1 = BaseModel()
        time = datetime.now()
        
        self.assertTrue(type(b1.id) is str)
        self.assertTrue(type(b1.created_at) is type(time))
        self.assertTrue(type(b1.updated_at) is type(time))

    def test_base_args(self):
        """ Test base model with args """

        b1 = BaseModel(1, 3) # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(b1.id is not None)
        self.assertTrue(b1.id != 1)
        self.assertTrue(b1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(b1.created_at is not None)
        self.assertTrue(b1.created_at != 1)
        self.assertTrue(b1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(b1.updated_at is not None)
        self.assertTrue(b1.updated_at != 1)
        self.assertTrue(b1.updated_at != 3)

    def test_base_kwargs(self):
        """ test base with kwargs """

        b1 = BaseModel()
        b1_dict = b1.to_dict()
        b2 = BaseModel(**b1_dict)

        self.assertEqual(b1.id, b2.id)
        self.assertEqual(b1.created_at, b2.created_at)
        self.assertEqual(b1.updated_at, b2.updated_at)
        self.assertTrue(b1 is not b2)

    def test_base_str(self):
        """ test __str__ method of base """

        b1 = BaseModel()
        out_str = "[{}] ({}) {}".format(
                 b1.__class__.__name__, b1.id, b1.__dict__
                )

        self.assertEqual(b1.__str__(), out_str)
