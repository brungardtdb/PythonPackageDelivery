import csv

import Data_Access.data_cleaner
from Models.location import Location
from Data_Structures.Graph.graph import Graph, Node, Edge
file_name = "Data/WGUPS Distance Table.csv"


# retrieves all locations from "WGUPS Distance Table.csv" file and returns locations in a graph
def get_locations():
    # using V to represent locations as vertices on a graph, so we can track locations separate from packages.
    # Time: O(v^2) to loop through each location for all given locations to find vertices and connecting edges
    # Space: O(v + e) where v is each location stored as a vertex and e is a connecting edge between vertices
    index = 0
    location_id = 1
    # loop through rows in csv file to create graph from distance list
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        num_locations = _get_num_locations()
        graph = Graph(num_locations)

        for row in reader:
            if index < 8:
                index += 1
                continue

            #  Create location
            location_name = row[0].split("\n")[0]
            location_address = row[1].split("\n")[0]
            loc = Location(
                location_id,
                location_name.strip(),
                Data_Access.data_cleaner.patch_package_address(location_address.strip())
            )

            # add location to node and insert node into graph
            node = Node(location_id, loc)
            graph.add_node(node)

            distance_list = []
            dist_index = 2
            # get the distance from this location to others if available
            while dist_index < num_locations + 2:
                distance = row[dist_index]
                empty_string = distance == ''
                zero = False
                if not empty_string:  # only try converting if not an empty string
                    zero = float(distance) == 0
                if not empty_string and not zero:  # only add distance if available and valid
                    d = float(distance)
                    distance_list.append(d)
                dist_index += 1

            # for each distance in distance list
            # create an edge from current node to connecting node
            loc_id = 1
            for dist in distance_list:
                other_loc = graph.get_node(loc_id)
                edge = Edge(node, other_loc, dist)
                graph.add_edge(edge)
                loc_id += 1

            location_id += 1
        return graph


# counts all the locations in "WGUPS Distance Table.csv"
def _get_num_locations():
    #  Time: O(v) linear time to read each line of the distance table and count them
    #  Space: O(1) constant space, we are only incrementing a single counter
    index = 0
    num_locations = 0
    # open csv file and read through each line, skipping first 8 (these are irrelevant)
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for _ in reader:
            # skip the first 8 lines that don't contain any useful data
            if index < 8:
                index += 1
                continue
            num_locations += 1

    return num_locations
