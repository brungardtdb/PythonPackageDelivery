from unittest import TestCase
from Data_Structures.KeyValueIndex.key_value_index import KeyValueIndex
import Data_Access.package_reader as pr


class TestHomeBrewDictionary(TestCase):
    def test_dictionary_insert(self):
        dict = KeyValueIndex(10)
        dict.add_item("foo", "bar")
        items = dict.get_items("foo")
        self.assertEqual("bar", items[0])

    def test_dictionary_double_insert(self):
        dict = KeyValueIndex(10)
        dict.add_item("foo", "bar")
        self.assertTrue(dict.add_item("foo", "batz"))
        items = dict.get_items("foo")
        self.assertEqual("bar", items[0])
        self.assertEqual("batz", items[1])