from unittest import TestCase
from Data_Structures.Hash_Map.hash_map import HashMap


class TestHashMap(TestCase):
    def test_append_item(self):
        hash_map = HashMap(3)
        self.assertTrue(hash_map.append_item(0, "foo"))
        self.assertTrue(hash_map.append_item(3, "bar"))
        self.assertFalse(hash_map.append_item(3, "baz"))
        self.assertEqual(str(hash_map.map), "[[(0, 'foo'), (3, 'bar')], [], []]")

    def test_remove_item(self):
        hash_map = HashMap(3)
        hash_map.append_item(0, "foo")
        hash_map.append_item(3, "bar")
        hash_map.append_item(3, "baz")
        self.assertTrue(hash_map.remove_item(3))
        self.assertFalse(hash_map.remove_item(3))
        self.assertEqual(str(hash_map.map), "[[(0, 'foo')], [], []]")

    def test_get_item(self):
        hash_map = HashMap(3)
        hash_map.append_item(0, "foo")
        hash_map.append_item(3, "bar")
        hash_map.append_item(3, "baz")
        test_item = hash_map.get_item(0)
        second_item = hash_map.get_item(3)
        self.assertEqual(test_item, "foo")
        self.assertEqual(second_item, "bar")

    def test_get_three_items(self):
        hash_map = HashMap(3)
        hash_map.append_item(1, "foo")
        hash_map.append_item(2, "bar")
        hash_map.append_item(3, "baz")
        first_item = hash_map.get_item(1)
        second_item = hash_map.get_item(2)
        third_item = hash_map.get_item(3)
        self.assertEqual(first_item, "foo")
        self.assertEqual(second_item, "bar")
        self.assertEqual(third_item, "baz")
