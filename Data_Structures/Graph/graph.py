from Data_Structures.Hash_Map.hash_map import HashMap
import math

# class to represent location graph
class Graph:
    # Time: O(v)
    # Space: O(v + e)
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.map = HashMap(num_nodes)

    # method for getting node from graph
    # Time: O(v)
    # Space: O(1)
    def get_node(self, node_id):
        node = self.map.get_item(node_id)
        if node is None:
            return None
        node = node
        return node

    # method for adding node to graph
    # Time: O(v)
    # Space: O(1)
    def add_node(self, node):
        self.map.append_item(node.id, node)

    # method for adding edge to graph
    # Time: O(v + e) to traverse all nodes and edges
    # Space: O(1) to add a single edge
    def add_edge(self, edge):
        #  prefer node with the lowest id #
        lowest_node = edge.first_node if edge.first_node.id < edge.second_node.id else edge.second_node
        highest_node = edge.second_node if edge.first_node.id < edge.second_node.id else edge.first_node

        #  ensure nodes exist
        if self.map.get_item(lowest_node.id) is None:
            self.add_node(lowest_node)  # O(v), O(1)
        if self.map.get_item(highest_node.id) is None:
            self.add_node(highest_node)  # O(v), O(1)

        #  get list in hashmap where node is stored
        first_node = self.map.get_item(lowest_node.id)  # O(v), O(1)
        second_node = self.map.get_item(highest_node.id)  # O(v), O(1)
        #  check if node already exists
        first_existing_edge = any(((lowest_node.id == edge.first_node.id)
                                  or (lowest_node.id == edge.second_node.id))
                                  and ((highest_node.id == edge.first_node.id)
                                  or (highest_node.id == edge.second_node.id))
                                  for edge in first_node.edges)  # O(e), O(1)
        second_existing_edge = any(((lowest_node.id == edge.first_node.id)
                                   or (lowest_node.id == edge.second_node.id))
                                   and ((highest_node.id == edge.first_node.id)
                                   or (highest_node.id == edge.second_node.id))
                                   for edge in second_node.edges)  # O(e), O(1)
        # add edge to node edge list
        if not first_existing_edge:
            first_node.edges.append(edge) # O(1), O(1)
        if not second_existing_edge:
            second_node.edges.append(edge) # O(1), O(1)

    # here lies several days of my available time to write this program
    # tragically I did not end up using this
    # perhaps the real treasure is the knowledge we learned along the way?
    def _traverse_node(self, current_node, search_map):
        lowest_cost_node = None
        lowest_cost = math.inf

        # get table row for current node
        current_node_row = search_map.get_item(current_node.id)

        # traverse each edge for current node
        for edge in current_node.edges:
            cost = edge.weight
            # figure out which node is connecting to current node
            other_node = edge.second_node if edge.second_node.id is not current_node.id else edge.first_node

            # get search result for connecting node, so we can update our table
            other_node_row = search_map.get_item(other_node.id)

            # if cost is less than current cost in table, update cost and parent in table
            total_cost = cost + current_node_row.cost
            if total_cost < other_node_row.cost:
                other_node_row.cost = total_cost  # be sure to account for total cost to get here
                other_node_row.parent_node = current_node

            # keep track of the lowest cost and lowest cost node, so we know which node to visit next
            if cost < lowest_cost and other_node_row.is_exhausted is False:
                lowest_cost = cost
                lowest_cost_node = other_node

        # update table for current node to reflect that it's edges have been exhausted
        current_node_row.is_exhausted = True

        # if we were unable to visit an adjacent node, try to find one we haven't visited
        if lowest_cost_node is None:
            for index in range(search_map.map_length):
                index += 1
                current_row = search_map.get_item(index)
                if current_row.is_exhausted is False:
                    lowest_cost_node = current_row.node
                    break

        # base case for recursion, return early if we don't have more nodes to visit
        if lowest_cost_node is None:
            return

        # traverse the next node
        self._traverse_node(lowest_cost_node, search_map)

    # here lies several days of my available time to write this program
    # tragically I did not end up using this
    # perhaps the real treasure is the knowledge we learned along the way?
    def get_dijkstras_shortest_path(self, starting_node):
        # create hashmap which will serve as a table to keep track of search results
        search_map = HashMap(self.map.map_length)
        # iterate through nodes, creating a row in the table for each node
        for index in range(self.map.map_length):
            index += 1
            current_node = self.get_node(index)
            if current_node is not None:
                if current_node.id is starting_node.id:
                    search_map.append_item(
                        current_node.id,         # no cost to visit starting node
                        self.DijkstraShortestPathTableRow(current_node, False, 0))
                else:
                    search_map.append_item(
                        current_node.id,  # initial cost for all other nodes is infinity
                        self.DijkstraShortestPathTableRow(current_node, False, math.inf))
        # begin recursively traversing nodes
        self._traverse_node(starting_node, search_map)

        # build the shortest distance graph from dijkstra's shortest path results
        result = Graph(self.num_nodes)
        # add a copy of each node
        for index in range(self.num_nodes):
            index += 1
            current_node = self.get_node(index)
            # note that we need a new node, so it will not have existing edges
            new_node = Node(current_node.id, current_node.data)
            result.add_node(new_node)
        # add edge for each node's shortest path
        for row_index in range(search_map.map_length):
            row_index += 1
            node_result = search_map.get_item(row_index)
            if node_result.parent_node is None:  # not necessary for starting node
                continue
            parent_cost = search_map.get_item(node_result.parent_node.id).cost
            cost = node_result.cost - parent_cost
            result_node = result.get_node(node_result.node.id)
            result_parent_node = result.get_node(node_result.parent_node.id)
            edge = Edge(result_node, result_parent_node, cost)
            result.add_edge(edge)
        return result

    class DijkstraShortestPathTableRow:
        def __init__(self, node, is_exhausted, cost):
            self.node = node
            self.is_exhausted = is_exhausted
            self.cost = cost
            self.parent_node = None  # will be assigned later


# class to represent nodes on graph
class Node:
    def __init__(self, node_id, data):
        self.id = node_id
        self.data = data
        self.edges = []


# class to represent edges on graph
class Edge:
    def __init__(self, first_node, second_node, weight):
        self.first_node = first_node
        self.second_node = second_node
        self.weight = weight
