from Data_Structures.KeyValueIndex.key_value_index import KeyValueIndex


# helper method used to ensure that any argument is a string
def _get_parameter_string_value(arg):
    # verify we are using a string as a key
    if isinstance(arg, str) is False:
        param = str(arg)
    else:
        param = arg
    return param


# package repository class to make searching for a package easier
# you can look up a package based on the address, deadline, city, etc.
# similar using a dictionary (which I was not allowed to use)
# we create a list to store the keys for packages based on different attributes
# this allows us to look up a package in O(1) time in the best and average case
# worst case for a hash map is O(n), I suppose there is no getting around that
class PackageRepository:

    def __init__(self, packages):
        self.packages = packages
        self.address_index = KeyValueIndex(self.packages.map_length)
        self.delivery_deadline_index = KeyValueIndex(self.packages.map_length)
        self.city_index = KeyValueIndex(self.packages.map_length)
        self.zip_code_index = KeyValueIndex(self.packages.map_length)
        self.mass_kilo_index = KeyValueIndex(self.packages.map_length)
        self.delivery_status_index = KeyValueIndex(self.packages.map_length)
        self.special_notes_index = KeyValueIndex(self.packages.map_length)
        self._index_packages()

    # method used to get package given the package id
    def get_package_by_id(self, package_id):
        return self.packages.get_item(package_id)

    # method used to get packages given an arbitrary search function to find the indices
    def _get_packages_by_search_criteria(self, search_function, search_parameter):
        result = []
        param = _get_parameter_string_value(search_parameter)
        # apply search function to obtain indices for matching packages
        indices = search_function(param)
        if indices is None:
            return result  # return early if we don't have a match
        # loop through indices and find corresponding package for each
        for index in indices:
            pkg = self.packages.get_item(index)
            if pkg is not None:
                result.append(pkg)
        return result

    # method used to get packages given the package address
    def get_packages_by_address(self, address):
        return self._get_packages_by_search_criteria(self.address_index.get_items, address)

    # method used to get packages given the delivery deadline
    def get_packages_by_delivery_deadline(self, deadline):
        return self._get_packages_by_search_criteria(self.delivery_deadline_index.get_items, deadline)

    # method used to get packages given the city for the package address
    def get_packages_by_city(self, city):
        return self._get_packages_by_search_criteria(self.city_index.get_items, city)

    # method used to get packages given the package zip code
    def get_packages_by_zip_code(self, zip_code):
        return self._get_packages_by_search_criteria(self.zip_code_index.get_items, zip_code)

    # method used to get packages given the package weight/mass kilo
    def get_packages_by_weight(self, weight):
        return self._get_packages_by_search_criteria(self.mass_kilo_index.get_items, weight)

    # method used to get packages given the package delivery status
    def get_packages_by_delivery_status(self, delivery_status):
        return self._get_packages_by_search_criteria(self.delivery_status_index.get_items, delivery_status)

    # method used to get packages given the package special notes
    def get_packages_by_special_notes(self, special_notes):
        return self._get_packages_by_search_criteria(self.special_notes_index.get_items, special_notes)

    # method used to create index for all packages in hash map
    def _index_packages(self):
        for package_groups in self.packages.map:
            for group in package_groups:
                self._index_package(group[1])

    # method used to index a package based on non id attributes
    def _index_package(self, package):
        self.address_index.add_item(
            _get_parameter_string_value(package.address), package.id
        )
        self.delivery_deadline_index.add_item(
            _get_parameter_string_value(package.delivery_deadline), package.id
        )
        self.city_index.add_item(
            _get_parameter_string_value(package.city), package.id
        )
        self.zip_code_index.add_item(
            _get_parameter_string_value(package.zip_code), package.id
        )
        self.mass_kilo_index.add_item(
            _get_parameter_string_value(package.mass_kilo), package.id
        )
        self.delivery_status_index.add_item(
            _get_parameter_string_value(package.delivery_status), package.id
        )
        self.special_notes_index.add_item(
            _get_parameter_string_value(package.special_notes), package.id
        )

# F.  Develop a look-up function that takes the following components
# as input and returns the corresponding data elements:
#   •  package ID number
#   •  delivery address
#   •  delivery deadline
#   •  delivery city
#   •  delivery zip code
#   •  package weight
#   •  delivery status (i.e., “at the hub,” “en route,” or “delivered”), including the delivery time
