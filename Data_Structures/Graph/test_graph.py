from unittest import TestCase
from Data_Structures.Graph.graph import Graph, Node, Edge


class TestGraph(TestCase):
    def test_add_node(self):
        graph = Graph(3)
        first_node = Node(1, "foo")
        second_node = Node(2, "bar")
        graph.add_node(first_node)
        graph.add_node(second_node)
        self.assertEqual(graph.map.map, [[], [(first_node.id, first_node)], [(second_node.id, second_node)]])

    def test_get_node(self):
        graph = Graph(3)
        first_node = Node(1, "foo")
        second_node = Node(2, "bar")
        third_node = Node(3, "baz")
        graph.add_node(first_node)
        graph.add_node(second_node)
        graph.add_node(third_node)
        node = graph.get_node(1)
        other_node = graph.get_node(2)
        another_node = graph.get_node(3)
        self.assertEqual(node, first_node)
        self.assertEqual(other_node, second_node)
        self.assertEqual(another_node, third_node)

    def test_add_edge(self):
        graph = Graph(3)
        first_node = Node(1, "foo")
        second_node = Node(2, "bar")
        edge = Edge(first_node, second_node, 3)
        graph.add_node(first_node)
        graph.add_node(second_node)
        graph.add_edge(edge)
        node_row = graph.map.map.__getitem__(1)
        node = node_row[0][1]
        self.assertEqual(node.edges[0], edge)

    def test_add_edge_twice(self):
        graph = Graph(3)
        first_node = Node(1, "foo")
        second_node = Node(2, "bar")
        edge = Edge(first_node, second_node, 3)
        second_edge = Edge(second_node, first_node, 3)
        graph.add_node(first_node)
        graph.add_node(second_node)
        graph.add_edge(edge)
        graph.add_edge(second_edge)
        node = graph.get_node(1)
        other_node = graph.get_node(2)
        self.assertEqual(len(node.edges), 1)

    def get_sample_graph(self):
        graph = Graph(9)

        # create nodes
        first_node = Node(1, "a")
        second_node = Node(2, "b")
        third_node = Node(3, "c")
        fourth_node = Node(4, "d")
        fifth_node = Node(5,"e")
        sixth_node = Node(6, "f")
        seventh_node = Node(7, "g")
        eighth_node = Node(8, "h")
        ninth_node = Node(9, "i")

        # create edges
        first_edge = Edge(first_node, second_node, 7)
        second_edge = Edge(first_node, third_node, 2)
        third_edge = Edge(first_node, fourth_node, 3)
        fourth_edge = Edge(second_node, sixth_node, 2)
        fifth_edge = Edge(sixth_node, fifth_node, 1)
        sixth_edge = Edge(third_node, seventh_node, 1)
        seventh_edge = Edge(seventh_node, fourth_node, 3)
        eighth_edge = Edge(seventh_node, eighth_node, 4)
        ninth_edge = Edge(fourth_node, fifth_node, 5)
        tenth_edge = Edge(fifth_node, ninth_node, 6)
        eleventh_edge = Edge(eighth_node, ninth_node, 2)

        # add nodes to graph
        graph.add_node(first_node)
        graph.add_node(second_node)
        graph.add_node(third_node)
        graph.add_node(fourth_node)
        graph.add_node(fifth_node)
        graph.add_node(sixth_node)
        graph.add_node(seventh_node)
        graph.add_node(eighth_node)
        graph.add_node(ninth_node)

        # add edges to graph
        graph.add_edge(first_edge)
        graph.add_edge(second_edge)
        graph.add_edge(third_edge)
        graph.add_edge(fourth_edge)
        graph.add_edge(fifth_edge)
        graph.add_edge(sixth_edge)
        graph.add_edge(seventh_edge)
        graph.add_edge(eighth_edge)
        graph.add_edge(ninth_edge)
        graph.add_edge(tenth_edge)
        graph.add_edge(eleventh_edge)

        return graph

    def get_shortest_path_sample_graph(self):
        graph = Graph(9)

        # create nodes
        first_node = Node(1, "a")
        second_node = Node(2, "b")
        third_node = Node(3, "c")
        fourth_node = Node(4, "d")
        fifth_node = Node(5,"e")
        sixth_node = Node(6, "f")
        seventh_node = Node(7, "g")
        eighth_node = Node(8, "h")
        ninth_node = Node(9, "i")

        # create edges
        first_edge = Edge(first_node, second_node, 7)
        second_edge = Edge(first_node, third_node, 2)
        third_edge = Edge(first_node, fourth_node, 3)
        fifth_edge = Edge(sixth_node, fifth_node, 1)
        sixth_edge = Edge(third_node, seventh_node, 1)
        eighth_edge = Edge(seventh_node, eighth_node, 4)
        ninth_edge = Edge(fourth_node, fifth_node, 5)
        eleventh_edge = Edge(eighth_node, ninth_node, 2)

        # add nodes to graph
        graph.add_node(first_node)
        graph.add_node(second_node)
        graph.add_node(third_node)
        graph.add_node(fourth_node)
        graph.add_node(fifth_node)
        graph.add_node(sixth_node)
        graph.add_node(seventh_node)
        graph.add_node(eighth_node)
        graph.add_node(ninth_node)

        # add edges to graph
        graph.add_edge(first_edge)
        graph.add_edge(second_edge)
        graph.add_edge(third_edge)
        graph.add_edge(fifth_edge)
        graph.add_edge(sixth_edge)
        graph.add_edge(eighth_edge)
        graph.add_edge(ninth_edge)
        graph.add_edge(eleventh_edge)

        return graph

    def test_get_shortest_path(self):

        graph = self.get_sample_graph()
        first_node = graph.get_node(1)
        shortest_path_graph = self.get_shortest_path_sample_graph()

        shortest_path_result = graph.get_dijkstras_shortest_path(first_node)

        self.assertEqual(shortest_path_graph.map.map_length, shortest_path_result.map.map_length)

        for index in range(shortest_path_graph.map.map_length):
            sp_node = shortest_path_graph.get_node(index)
            result_node = shortest_path_result.get_node(index)
            if sp_node is None and result_node is None:
                continue
            self.assertEqual(len(sp_node.edges), len(result_node.edges))
            self.assertEqual(sp_node.id, result_node.id)
            self.assertEqual(sp_node.data, result_node.data)
            for edge_index in range(len(sp_node.edges)):
                sp_edge = sp_node.edges[edge_index]
                result_edge = result_node.edges[edge_index]
                has_match = any((item.first_node.id is result_edge.first_node.id or
                                 item.first_node.id is result_edge.second_node.id) and
                                (item.second_node.id is result_edge.first_node.id or
                                 item.second_node.id is result_edge.second_node.id)
                                for item in sp_node.edges)
                self.assertTrue(has_match)
                matching_edge = None
                for item in sp_node.edges:
                    is_match = ((item.first_node.id is result_edge.first_node.id or
                                 item.first_node.id is result_edge.second_node.id) and
                                (item.second_node.id is result_edge.first_node.id or
                                 item.second_node.id is result_edge.second_node.id))
                    if is_match:
                        matching_edge = item
                        break
                self.assertFalse(matching_edge is None)
                self.assertTrue(sp_edge.weight, matching_edge.weight)


