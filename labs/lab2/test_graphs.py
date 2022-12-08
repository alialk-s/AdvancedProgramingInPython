import unittest
from graphs import *


class TestGraphs(unittest.TestCase):

    def setUp(self):
        self.edges = [(1, 2), (5, 2), (6, 1), (8, 5), (11, 4), (7, 4)]
        self.graph = Graph(self.edges)

    def test_both_all_vertices_exist(self):
        for (a, b) in self.graph.edges():
            self.assertIn(a, self.graph.vertices())
            self.assertIn(b, self.graph.vertices())

    def test_both_neighbours_exist(self):
        for a in self.graph.vertices():
            for b in self.graph.vertices():
                if a in self.graph.neighbors(b):
                    self.assertIn(b, self.graph.neighbors(a))

    def test_remove_vertex(self):
        self.graph.remove_vertex(11)
        self.assertTrue(11 not in self.graph.vertices())

    def test_associated_edges_after_removing_vertex(self):
        self.graph.remove_vertex(4)
        self.assertTrue((11, 4) not in self.graph.edges() and (7, 4) not in self.graph.edges())

    def test_add_edge(self):
        self.graph.add_edge(5, 4)
        self.assertIn((5, 4), self.graph.edges())

    def test_add_edge_with_non_existing_vertices(self):
        self.graph.add_edge(20, 15)
        self.assertIn((20, 15), self.graph.edges())
        self.assertIn(20, self.graph.vertices())
        self.assertIn(15, self.graph.vertices())



if __name__ == '__main__':
    unittest.main()
