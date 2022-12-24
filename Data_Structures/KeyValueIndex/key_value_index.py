from Data_Structures.Hash_Map.hash_map import HashMap


def _validate_key_string(key):
    if isinstance(key, str) is False:
        raise ValueError("Index key must be a string")


# class used to store keys for a particular value
# works sort of like a dictionary
# only the mapping is one-to-many, not one-to-one
# this will allow us for quick look up for items in a hash map
# based non-key attributes (like strings)
class KeyValueIndex:

    def __init__(self, num_items):
        self.num_items = num_items
        self.map = HashMap(num_items)
        #  initialize each hashmap value to list to account for collisions
        for index in range(self.num_items):
            self.map.append_item(index, [])

    class DictionaryEntry:

        def __init__(self, key, data):
            self.key = key
            self.data = data

    # used to add item to the index based on defining value or attribute
    def add_item(self, key, value):
        entry = self.DictionaryEntry(key, value)
        _validate_key_string(key)
        index = self._hash_string(key)
        entry_slot = self.map.get_item(index)
        # if index is empty, add item
        if len(entry_slot) == 0:
            entry_slot.append(entry)
            return True
        # verify key is not already used in index
        for e in entry_slot:
            if e.data is value:
                return False
        # if key is available, add item
        entry_slot.append(entry)
        return True

    # used to get item based on defining value or attribute
    def get_items(self, key):
        _validate_key_string(key)
        index = self._hash_string(key)
        entry_slot = self.map.get_item(index)
        # if index is empty, return none
        if len(entry_slot) == 0:
            return None
        result = []
        # iterate through items in index and return corresponding item
        for entry in entry_slot:
            if entry.key == key:
                result.append(entry.data)
        if len(result) > 0:
            return result
        return None  # if not found

    # used to create an index from a string
    # takes the absolute value of a hashed string
    # and uses the remainder after dividing by the number of items
    def _hash_string(self, string):
        return abs(hash(string)) % self.num_items
