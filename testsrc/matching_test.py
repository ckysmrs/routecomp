import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from edge import Edge
from alias_graph import AliasGraph
from matching import blossom

class MatchingTest(unittest.TestCase):
    def setUp(self):
        self.complete_graph = AliasGraph()

        self.complete_graph.add_edge(Edge(0, 1, Decimal('0.6')))
        self.complete_graph.add_edge(Edge(0, 2, Decimal('1.2')))
        self.complete_graph.add_edge(Edge(0, 3, Decimal('1.3')))
        self.complete_graph.add_edge(Edge(0, 4, Decimal('1.4')))
        self.complete_graph.add_edge(Edge(0, 5, Decimal('1.1')))
        self.complete_graph.add_edge(Edge(1, 2, Decimal('0.7')))
        self.complete_graph.add_edge(Edge(1, 3, Decimal('1.7')))
        self.complete_graph.add_edge(Edge(1, 4, Decimal('1.6')))
        self.complete_graph.add_edge(Edge(1, 5, Decimal('1.5')))
        self.complete_graph.add_edge(Edge(2, 3, Decimal('0.8')))
        self.complete_graph.add_edge(Edge(2, 4, Decimal('1.9')))
        self.complete_graph.add_edge(Edge(2, 5, Decimal('1.8')))
        self.complete_graph.add_edge(Edge(3, 4, Decimal('0.9')))
        self.complete_graph.add_edge(Edge(3, 5, Decimal('2.0')))
        self.complete_graph.add_edge(Edge(4, 5, Decimal('1.0')))

    def test_blossom(self):
        # 完全グラフから最小コスト最大マッチングを返す
        act = blossom(self.complete_graph)
        self.assertEqual(act.get_node_size(), 6)
        self.assertEqual(act.get_edge_size(), 3)
        self.assertIsNotNone(act.get_edge_by_real_nodes(0, 1))
        self.assertIsNotNone(act.get_edge_by_real_nodes(2, 3))
        self.assertIsNotNone(act.get_edge_by_real_nodes(4, 5))
