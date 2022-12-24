class HashMap:

    def __init__(self, map_length):
        self.map_length = map_length
        self.map = []

        # initialize hashmap
        for item in range(map_length):
            self.map.append([])

    # Method used to retrieve item from hash map
    def get_item(self, key):
        index = key % self.map_length
        map_slot = self.map[index]
        # if slot is empty or item with matching key does not exist in slot, return None
        if (len(map_slot) == 0) or not any(key in k for k in map_slot):
            return None
        for item in map_slot:
            if item[0] == key:
                return item[1]
        return None  # just to be safe, return none if not found, previous check should account for this

    # Method used to add item to hash map
    def append_item(self, key, item):
        index = key % self.map_length
        map_slot = self.map[index]
        # if slot is empty or item with matching key does not exist in slot
        if (len(map_slot) == 0) or not any(key in k for k in map_slot):
            map_slot.append((key, item))
            return True
        return False  # if item with that key already exists and append is unsuccessful

    # Method used to remove item from hash map
    def remove_item(self, key):
        index = key % self.map_length
        map_slot = self.map[index]
        # check if slot is not empty and item with matching key is in slot
        if (len(map_slot) != 0) and any(key in k for k in map_slot):
            # if we have a match, find item and remove
            for i in range(len(map_slot)):
                if map_slot[i][0] == key:
                    del map_slot[i]
                    return True
        return False  # if slot is empty or item not found

# Develop a hash table, without using any additional libraries or classes,
# that has an insertion function that takes the following components as input
# and inserts the components into the hash table:
#   •  package ID number
#   •  delivery address
#   •  delivery deadline
#   •  delivery city
#   •  delivery zip code
#   •  package weight
#   •  delivery status (e.g., delivered, en route)
