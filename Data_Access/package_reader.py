import csv

import Data_Access.data_cleaner
from Data_Structures.Hash_Map.hash_map import HashMap
from Models.package import Package
from datetime import datetime
file_name = "Data/WGUPS Package File.csv"


# converts a string to time
# If "EOD" just returns "EOD" since we cannot convert text to time
def _string_to_time(t):
    if t == "EOD":
        return t
    time = datetime.strptime(t, '%H:%M %p').time()
    return time


# retrieves all packages from "WGUPS Package File.csv" file and returns packages in a list
def get_packages(file=file_name):

    # Time: O(n) linear time to read each line of the package file
    # Space: O(n) linear space to create an entry in the hash map for every package
    index = 0
    # open csv file and read through each line, skipping first 8 (these are irrelevant)
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        num_packages = __get_num_packages(file)
        hash_map = HashMap(num_packages)

        for row in reader:
            # skip the first 8 lines that don't contain any useful data
            if index < 8:
                index += 1
                continue
            # create new package for each row and append to a list
            hash_map.append_item(
                int(row[0]),
                Package(
                    int(row[0]),
                    Data_Access.data_cleaner.patch_package_address(row[1].strip()),
                    row[2].strip(),
                    row[4].strip(),
                    _string_to_time(row[5].strip()),
                    row[6].strip(),
                    row[7].strip()
                )
            )
    return hash_map


# counts all packages in "WGUPS Package File.csv"
def __get_num_packages(file=file_name):
    # Time: O(n) linear time to read each line of the package file and count the packages
    #  Space: O(1) constant space, we are only incrementing a single counter
    index = 0
    num_packages = 0
    # open csv file and read through each line, skipping first 8 (these are irrelevant)
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for _ in reader:
            # skip the first 8 lines that don't contain any useful data
            if index < 8:
                index += 1
                continue
            num_packages += 1

    return num_packages
