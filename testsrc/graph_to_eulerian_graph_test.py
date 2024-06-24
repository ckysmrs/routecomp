import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from edge import Edge
from alias_graph import AliasGraph
import graph_to_eulerian_graph

class EulerCircuitSolverTest(unittest.TestCase):
    def test_make_complete_graph(self):
        # 完全グラフを作成する
        graph = AliasGraph()
        graph.add_edge(Edge(0, 1, Decimal('4')))
        graph.add_edge(Edge(0, 2, Decimal('1')))
        graph.add_edge(Edge(0, 3, Decimal('3')))
        graph.add_edge(Edge(1, 2, Decimal('2')))
        graph.add_edge(Edge(2, 4, Decimal('5')))
        nodes = [1, 3, 4]
        g = graph_to_eulerian_graph.make_complete_graph(nodes, graph)
        self.assertEqual(g.get_edge_size(), 3)
        self.assertEqual(g.get_node_size(), 3)
        self.assertTrue(g.contains_edge(Edge(1, 3, Decimal('6'))))
        self.assertTrue(g.contains_edge(Edge(1, 4, Decimal('7'))))
        self.assertTrue(g.contains_edge(Edge(3, 4, Decimal('9'))))

    def test_get_odd_degree_nodes(self):
        # 次数が奇数のノードリストを返す
        graph = AliasGraph()
        graph.add_edge(Edge(0, 1, Decimal('4')))
        graph.add_edge(Edge(0, 2, Decimal('1')))
        graph.add_edge(Edge(1, 2, Decimal('2')))
        graph.add_edge(Edge(2, 4, Decimal('5')))
        nodes = graph_to_eulerian_graph.get_odd_degree_nodes(graph)
        self.assertEqual(len(nodes), 2)
        self.assertTrue(2 in nodes)
        self.assertTrue(4 in nodes)

    def test_add_matching_to_graph(self):
        # 始点と終点を指定して最短距離の辺を追加する
        org_graph = AliasGraph()
        org_graph.add_edge(Edge(0, 1, Decimal('10')))
        org_graph.add_edge(Edge(0, 2, Decimal('8')))
        org_graph.add_edge(Edge(1, 2, Decimal('9')))
        org_graph.add_edge(Edge(2, 3, Decimal('7')))
        org_graph.add_edge(Edge(3, 4, Decimal('1')))
        org_graph.add_edge(Edge(3, 5, Decimal('3')))
        org_graph.add_edge(Edge(3, 6, Decimal('5')))
        org_graph.add_edge(Edge(4, 7, Decimal('2')))
        org_graph.add_edge(Edge(5, 7, Decimal('6')))
        org_graph.add_edge(Edge(6, 7, Decimal('4')))
        ext_graph = AliasGraph()
        ext_graph.add_edge(Edge(2, 7, Decimal('1')))
        exp_graph = AliasGraph.copy_instance(org_graph)
        exp_graph.add_edge(Edge(2, 3, Decimal('7')))
        exp_graph.add_edge(Edge(3, 4, Decimal('1')))
        exp_graph.add_edge(Edge(4, 7, Decimal('2')))
        graph_to_eulerian_graph.add_matching_to_graph(ext_graph, org_graph)
        self.assertEqual(org_graph, exp_graph)

    def test_make_euler_graph(self):
        # オイラーグラフを作成する
        org_graph = AliasGraph()
        org_graph.add_edge(Edge(0, 1, Decimal('10')))
        org_graph.add_edge(Edge(0, 2, Decimal('8')))
        org_graph.add_edge(Edge(1, 2, Decimal('9')))
        org_graph.add_edge(Edge(2, 3, Decimal('7')))
        org_graph.add_edge(Edge(3, 4, Decimal('1')))
        org_graph.add_edge(Edge(3, 5, Decimal('3')))
        org_graph.add_edge(Edge(3, 6, Decimal('5')))
        org_graph.add_edge(Edge(4, 7, Decimal('2')))
        org_graph.add_edge(Edge(5, 7, Decimal('6')))
        org_graph.add_edge(Edge(6, 7, Decimal('4')))
        exp_graph = AliasGraph.copy_instance(org_graph)
        exp_graph.add_edge(Edge(2, 3, Decimal('7')))
        exp_graph.add_edge(Edge(3, 4, Decimal('1')))
        exp_graph.add_edge(Edge(4, 7, Decimal('2')))
        graph_to_eulerian_graph.make_euler_graph(org_graph)
        self.assertEqual(org_graph, exp_graph)

    def test_restore_branch_with_duplicating(self):
        # 枝線を複製しながらマージする
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('1')))
        g1 = AliasGraph()
        g1.add_edge(Edge(1, 2, Decimal('1')))
        g1.set_alias_node(2, 5)
        g2 = AliasGraph()
        g2.add_edge(Edge(3, 4, Decimal('1')))
        g2.set_alias_node(3, 5)
        graph_to_eulerian_graph.restore_branch_with_duplicating(sut, [g2, g1])
        self.assertEqual(sut.get_node_size(), 4)
        self.assertEqual(sut.get_real_node_size(), 5)
        self.assertEqual(sut.get_edge_size(), 5)

    def test_graph_to_eulerian_graph(self):
        # オイラーグラフを生成する
        g = AliasGraph()
        e1 = Edge(0, 4, Decimal('0.1'))
        g.add_edge(e1)
        e2 = Edge(1, 4, Decimal('0.2'))
        g.add_edge(e2)
        g.add_edge(Edge(0, 3, Decimal('0.3')))
        g.add_edge(Edge(1, 3, Decimal('0.4')))
        e5 = Edge(2, 3, Decimal('0.5'))
        g.add_edge(e5)
        g.add_edge(Edge(0, 1, Decimal('0.6')))
        act = graph_to_eulerian_graph.graph_to_eulerian_graph(g)
        self.assertEqual(act.get_edge_size(), 9)
        self.assertEqual(act.get_number_of_edge(e1), 2)
        self.assertEqual(act.get_number_of_edge(e2), 2)
        self.assertEqual(act.get_number_of_edge(e5), 2)
