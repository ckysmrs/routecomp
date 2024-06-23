import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from blossom_matching import BlossomMatching
from matching_graph import MatchingGraph

class BlossomMatchingTest(unittest.TestCase):
    def test_min_weight_matching(self):
        # コスト最小最大マッチングを返す
        graph = MatchingGraph(10)
        cost: list[Decimal] = []
        for i in range(16):
            cost.append(Decimal(0))
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 2)
        graph.add_edge(1, 5)
        graph.add_edge(1, 6)
        graph.add_edge(2, 3)
        graph.add_edge(2, 4)
        graph.add_edge(3, 4)
        graph.add_edge(4, 6)
        graph.add_edge(4, 7)
        graph.add_edge(4, 8)
        graph.add_edge(5, 6)
        graph.add_edge(6, 7)
        graph.add_edge(7, 8)
        graph.add_edge(7, 9)
        graph.add_edge(8, 9)
        cost[graph.get_edge_index(0, 1)] = Decimal(10)
        cost[graph.get_edge_index(0, 2)] = Decimal(4)
        cost[graph.get_edge_index(1, 2)] = Decimal(3)
        cost[graph.get_edge_index(1, 5)] = Decimal(2)
        cost[graph.get_edge_index(1, 6)] = Decimal(2)
        cost[graph.get_edge_index(2, 3)] = Decimal(1)
        cost[graph.get_edge_index(2, 4)] = Decimal(2)
        cost[graph.get_edge_index(3, 4)] = Decimal(5)
        cost[graph.get_edge_index(4, 6)] = Decimal(4)
        cost[graph.get_edge_index(4, 7)] = Decimal(1)
        cost[graph.get_edge_index(4, 8)] = Decimal(3)
        cost[graph.get_edge_index(5, 6)] = Decimal(1)
        cost[graph.get_edge_index(6, 7)] = Decimal(2)
        cost[graph.get_edge_index(7, 8)] = Decimal(3)
        cost[graph.get_edge_index(7, 9)] = Decimal(2)
        cost[graph.get_edge_index(8, 9)] = Decimal(1)
        matcher = BlossomMatching(graph)
        solution: tuple[list[int], Decimal] = matcher.solve_minimum_cost_perfect_matching(cost)
        self.assertEqual(14, solution[1])
        matching = solution[0]
        self.assertEqual(5, len(matching))
        results: list[tuple[int, int]] = []
        for i in matching:
            results.append(graph.get_edge(i))
        self.assertTrue(self.contains_pair(results, 0, 1))
        self.assertTrue(self.contains_pair(results, 2, 3))
        self.assertTrue(self.contains_pair(results, 4, 7))
        self.assertTrue(self.contains_pair(results, 5, 6))
        self.assertTrue(self.contains_pair(results, 8, 9))

    def test_min_weight_matching2(self):
        # コスト最小最大マッチングを返す(その2)
        graph = MatchingGraph(8)
        cost: list[Decimal] = []
        for i in range(16):
            cost.append(Decimal(0))
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(0, 3)
        graph.add_edge(0, 7)
        graph.add_edge(1, 2)
        graph.add_edge(1, 5)
        graph.add_edge(1, 7)
        graph.add_edge(2, 3)
        graph.add_edge(2, 5)
        graph.add_edge(2, 6)
        graph.add_edge(3, 4)
        graph.add_edge(3, 5)
        graph.add_edge(4, 5)
        graph.add_edge(5, 6)
        graph.add_edge(5, 7)
        graph.add_edge(6, 7)
        cost[graph.get_edge_index(0, 1)] = Decimal(8)
        cost[graph.get_edge_index(0, 2)] = Decimal(10)
        cost[graph.get_edge_index(0, 3)] = Decimal(4)
        cost[graph.get_edge_index(0, 7)] = Decimal(4)
        cost[graph.get_edge_index(1, 2)] = Decimal(8)
        cost[graph.get_edge_index(1, 5)] = Decimal(8)
        cost[graph.get_edge_index(1, 7)] = Decimal(11)
        cost[graph.get_edge_index(2, 3)] = Decimal(8)
        cost[graph.get_edge_index(2, 5)] = Decimal(8)
        cost[graph.get_edge_index(2, 6)] = Decimal(14)
        cost[graph.get_edge_index(3, 4)] = Decimal(13)
        cost[graph.get_edge_index(3, 5)] = Decimal(10)
        cost[graph.get_edge_index(4, 5)] = Decimal(12)
        cost[graph.get_edge_index(5, 6)] = Decimal(12)
        cost[graph.get_edge_index(5, 7)] = Decimal(9)
        cost[graph.get_edge_index(6, 7)] = Decimal(13)
        matcher = BlossomMatching(graph)
        solution: tuple[list[int], Decimal] = matcher.solve_minimum_cost_perfect_matching(cost)
        self.assertEqual(37, solution[1])
        matching = solution[0]
        self.assertEqual(4, len(matching))
        results: list[tuple[int, int]] = []
        for i in matching:
            results.append(graph.get_edge(i))
        self.assertTrue(self.contains_pair(results, 0, 3))
        self.assertTrue(self.contains_pair(results, 1, 2))
        self.assertTrue(self.contains_pair(results, 4, 5))
        self.assertTrue(self.contains_pair(results, 6, 7))

    def contains_pair(self, list: list[tuple[int, int]], x: int, y: int) -> bool:
        for p in list:
            if (p[0] == x and p[1] == y) or (p[0] == y and p[1] == x):
                return True
        return False
