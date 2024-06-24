import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from alias_graph import AliasGraph
import graph_file_loader

class GraphFileLoaderTest(unittest.TestCase):
    def test_load_data(self):
        # ファイルデータを読む
        graph = AliasGraph()
        transfer_list: list[set[int]] = []
        test_file = os.path.join(os.path.dirname(__file__), 'route_data/graph_file_loader_test.txt')
        self.assertTrue(graph_file_loader.load_data(graph, [test_file], transfer_list))
        self.assertEqual(graph.get_edge_size(), 5)
        self.assertEqual(graph.get_node_size(), 6)
        self.assertFalse(graph.is_connected())
