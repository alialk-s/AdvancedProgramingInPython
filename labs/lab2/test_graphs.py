import unittest
from graphs import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def setUp(self):
        self.edges = [(1, 2), (5, 2), (6, 1), (8, 5), (11, 4), (7, 4), (3, 4)]
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


if __name__ == '__main__':
    unittest.main()
