import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from dijkstra import get_shortest_length
from dijkstra import single_source_shortest_length
from dijkstra import get_shortest_path
from dijkstra import set_costs_to_goals
from dijkstra import make_node_list
from edge import Edge
from alias_graph import AliasGraph

class DijkstraTest(unittest.TestCase):
    def setUp(self):
        self.g = AliasGraph()
        self.g.add_edge(Edge(0, 1, Decimal('2')))
        self.g.add_edge(Edge(1, 2, Decimal('1')))
        self.g.add_edge(Edge(2, 7, Decimal('6')))
        self.g.add_edge(Edge(7, 6, Decimal('1')))
        self.g.add_edge(Edge(6, 5, Decimal('2')))
        self.g.add_edge(Edge(5, 4, Decimal('1')))
        self.g.add_edge(Edge(4, 0, Decimal('4')))
        self.g.add_edge(Edge(0, 3, Decimal('6')))
        self.g.add_edge(Edge(3, 6, Decimal('3')))
        self.g.add_edge(Edge(3, 4, Decimal('1')))
        self.g.add_edge(Edge(1, 7, Decimal('8')))

    def test_get_shortest_length(self):
        self.assertEqual(get_shortest_length(self.g, 0, 1), 2)
        self.assertEqual(get_shortest_length(self.g, 0, 2), 3)
        self.assertEqual(get_shortest_length(self.g, 0, 3), 5)
        self.assertEqual(get_shortest_length(self.g, 0, 4), 4)
        self.assertEqual(get_shortest_length(self.g, 0, 5), 5)
        self.assertEqual(get_shortest_length(self.g, 0, 6), 7)
        self.assertEqual(get_shortest_length(self.g, 0, 7), 8)
        self.assertEqual(get_shortest_length(self.g, 1, 2), 1)
        self.assertEqual(get_shortest_length(self.g, 1, 3), 7)
        self.assertEqual(get_shortest_length(self.g, 1, 4), 6)
        self.assertEqual(get_shortest_length(self.g, 1, 5), 7)
        self.assertEqual(get_shortest_length(self.g, 1, 6), 8)
        self.assertEqual(get_shortest_length(self.g, 1, 7), 7)
        self.assertEqual(get_shortest_length(self.g, 2, 3), 8)
        self.assertEqual(get_shortest_length(self.g, 2, 4), 7)
        self.assertEqual(get_shortest_length(self.g, 2, 5), 8)
        self.assertEqual(get_shortest_length(self.g, 2, 6), 7)
        self.assertEqual(get_shortest_length(self.g, 2, 7), 6)
        self.assertEqual(get_shortest_length(self.g, 3, 4), 1)
        self.assertEqual(get_shortest_length(self.g, 3, 5), 2)
        self.assertEqual(get_shortest_length(self.g, 3, 6), 3)
        self.assertEqual(get_shortest_length(self.g, 3, 7), 4)
        self.assertEqual(get_shortest_length(self.g, 4, 5), 1)
        self.assertEqual(get_shortest_length(self.g, 4, 6), 3)
        self.assertEqual(get_shortest_length(self.g, 4, 7), 4)
        self.assertEqual(get_shortest_length(self.g, 5, 6), 2)
        self.assertEqual(get_shortest_length(self.g, 5, 7), 3)
        self.assertEqual(get_shortest_length(self.g, 6, 7), 1)

    def test_get_shortest_length_last(self):
        # ゴール直前に逆転するコストがある場合
        g = AliasGraph()
        g.add_edge(Edge(0, 1, Decimal(1)))
        g.add_edge(Edge(0, 2, Decimal(10)))
        g.add_edge(Edge(1, 3, Decimal(100)))
        g.add_edge(Edge(2, 3, Decimal(1)))
        self.assertEqual(get_shortest_length(g, 0, 3), 11)

    def test_single_source_shortest_length(self):
        goals = list(range(8))
        self.assertEqual(single_source_shortest_length(self.g, 0, goals), [0, 2, 3, 5, 4, 5, 7, 8])
        self.assertEqual(single_source_shortest_length(self.g, 1, goals), [2, 0, 1, 7, 6, 7, 8, 7])
        self.assertEqual(single_source_shortest_length(self.g, 2, goals), [3, 1, 0, 8, 7, 8, 7, 6])
        self.assertEqual(single_source_shortest_length(self.g, 3, goals), [5, 7, 8, 0, 1, 2, 3, 4])
        self.assertEqual(single_source_shortest_length(self.g, 4, goals), [4, 6, 7, 1, 0, 1, 3, 4])
        self.assertEqual(single_source_shortest_length(self.g, 5, goals), [5, 7, 8, 2, 1, 0, 2, 3])
        self.assertEqual(single_source_shortest_length(self.g, 6, goals), [7, 8, 7, 3, 3, 2, 0, 1])
        self.assertEqual(single_source_shortest_length(self.g, 7, goals), [8, 7, 6, 4, 4, 3, 1, 0])

    def test_get_shortest_path(self):
        path = get_shortest_path(self.g, 0, 7)
        self.assertEqual(len(path), 5)
        if len(path) == 5:
            self.assertEqual(path[0].get_id(), 0)
            self.assertEqual(path[1].get_id(), 4)
            self.assertEqual(path[2].get_id(), 5)
            self.assertEqual(path[3].get_id(), 6)
            self.assertEqual(path[4].get_id(), 7)

    def test_get_shortest_path_same(self):
        # スタートとゴールが同じ経路探索
        path = get_shortest_path(self.g, 0, 0)
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0].get_id(), 0)

    def test_set_costs_to_goals(self):
        # ダイクストラ法でゴールのコストを計算する
        goals = set_costs_to_goals(self.g, 0, list(range(8)))
        act = [n.get_score() for n in goals]
        exp = [0, 2, 3, 5, 4, 5, 7, 8]
        self.assertEqual(act, exp)

    def test_make_node_list(self):
        l = make_node_list(self.g)
        self.assertEqual(len(l), 8)
