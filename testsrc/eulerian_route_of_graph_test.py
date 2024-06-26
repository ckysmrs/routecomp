import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from edge import Edge
from alias_graph import AliasGraph
from eulerian_route_of_graph import generate_loop_route
from eulerian_route_of_graph import merge_euler_circuit
from eulerian_route_of_graph import select_start_node
from eulerian_route_of_graph import add_alias_connect

class EulerianRouteOfGraphTest(unittest.TestCase):
    def test_generate_loop_route(self):
        g = AliasGraph()
        g.add_edge(Edge(0, 1, Decimal('1')))
        g.add_edge(Edge(0, 3, Decimal('1')))
        g.add_edge(Edge(1, 2, Decimal('1')))
        g.add_edge(Edge(1, 3, Decimal('1')))
        g.add_edge(Edge(1, 4, Decimal('1')))
        g.add_edge(Edge(2, 3, Decimal('1')))
        g.add_edge(Edge(2, 4, Decimal('1')))
        g.add_edge(Edge(2, 5, Decimal('1')))
        g.add_edge(Edge(3, 5, Decimal('1')))
        g_bk = AliasGraph.copy_instance(g)
        route = generate_loop_route(g, 0)
        self.assertEqual(g_bk.get_alias_node(route[0][0]), 0)
        for i in range(1, len(route)):
            self.assertEqual(g_bk.get_alias_node(route[i - 1][1]), g_bk.get_alias_node(route[i][0]))
        self.assertEqual(g_bk.get_alias_node(route[-1][1]), 0)

    def test_generate_loop_route_alias(self):
        # エイリアスを始点にしてループルートを探索
        g = AliasGraph()
        g.add_edge(Edge(0, 1, Decimal('1')))
        g.add_edge(Edge(1, 2, Decimal('1')))
        g.add_edge(Edge(0, 2, Decimal('1')))
        g.add_edge(Edge(3, 4, Decimal('1')))
        g.add_edge(Edge(4, 5, Decimal('1')))
        g.add_edge(Edge(3, 5, Decimal('1')))
        g.set_alias_node(0, 6)
        g.set_alias_node(3, 6)
        g_bk = AliasGraph.copy_instance(g)
        route = generate_loop_route(g, 0)
        self.assertEqual(g_bk.get_alias_node(route[0][0]), 6)
        for i in range(1, len(route)):
            self.assertEqual(g_bk.get_alias_node(route[i - 1][1]), g_bk.get_alias_node(route[i][0]))
        self.assertEqual(g_bk.get_alias_node(route[-1][1]), 6)

    def test_generate_loop_route_alias_one(self):
        # ノード2つをエイリアス設定したときのループ探索
        g = AliasGraph()
        g.add_edge(Edge(0, 1, Decimal('1')))
        g.set_alias_node(0, 2)
        g.set_alias_node(1, 2)
        g_bk = AliasGraph.copy_instance(g)
        route = generate_loop_route(g, 0)
        self.assertEqual(g_bk.get_alias_node(route[0][0]), 2)
        self.assertEqual(g_bk.get_alias_node(route[0][1]), 2)

    def test_generate_loop_via_alias(self):
        # エイリアスを通るループ探索
        # 1-2=3-1のループ
        g = AliasGraph()
        g.add_edge(Edge(1, 2, Decimal('1')))
        g.add_edge(Edge(3, 1, Decimal('1')))
        g.set_alias_node(2, 11)
        g.set_alias_node(3, 11)
        g_bk = AliasGraph.copy_instance(g)
        route = generate_loop_route(g, 1)
        self.assertEqual(g_bk.get_alias_node(route[0][0]), 1)
        self.assertEqual(g_bk.get_alias_node(route[-1][1]), 1)
        self.assertEqual(len(route), 2)

    def test_merge_euler_circuit(self):
        nodes = [i for i in range(6)]
        route1 = [[nodes[i], nodes[(i + 1) % 4]] for i in range(4)]
        route2 = [[nodes[1], nodes[4]], [nodes[4], nodes[5]], [nodes[5], nodes[1]]]
        merge_euler_circuit(route1, route2, AliasGraph())
        self.assertEqual(route1[0], [nodes[0], nodes[1]])
        self.assertEqual(route1[1], [nodes[1], nodes[4]])
        self.assertEqual(route1[2], [nodes[4], nodes[5]])
        self.assertEqual(route1[3], [nodes[5], nodes[1]])
        self.assertEqual(route1[4], [nodes[1], nodes[2]])
        self.assertEqual(route1[5], [nodes[2], nodes[3]])
        self.assertEqual(route1[6], [nodes[3], nodes[0]])

    def test_select_start_node_initial_start(self):
        # 最初のスタートノード探索で、スタートノードを指定したとき
        g = AliasGraph()
        g.add_edge(Edge(0, 1, Decimal(1)))
        g.add_edge(Edge(1, 2, Decimal(1)))
        g.add_edge(Edge(2, 0, Decimal(1)))
        g.add_edge(Edge(3, 4, Decimal(1)))
        g.add_edge(Edge(4, 5, Decimal(1)))
        g.add_edge(Edge(5, 3, Decimal(1)))
        g.set_alias_node(2, 6)
        g.set_alias_node(3, 6)
        self.assertEqual(select_start_node(g, [], 2), 2)
        
    def test_select_start_node_initial(self):
        # 最初のスタートノード探索で、スタートノードを指定しないとき
        g = AliasGraph()
        g.add_edge(Edge(0, 1, Decimal(1)))
        g.add_edge(Edge(1, 2, Decimal(1)))
        g.add_edge(Edge(2, 0, Decimal(1)))
        g.add_edge(Edge(3, 4, Decimal(1)))
        g.add_edge(Edge(4, 5, Decimal(1)))
        g.add_edge(Edge(5, 3, Decimal(1)))
        g.set_alias_node(2, 6)
        g.set_alias_node(3, 6)
        self.assertTrue(select_start_node(g, [], -1) in (0, 1, 2, 3, 4, 5))

    def test_select_start_node(self):
        # スタートノード探索
        g = AliasGraph()
        e1 = Edge(0, 1, Decimal(1))
        g.add_edge(e1)
        e2 = Edge(1, 2, Decimal(1))
        g.add_edge(e2)
        e3 = Edge(2, 0, Decimal(1))
        g.add_edge(e3)
        g.add_edge(Edge(3, 4, Decimal(4)))
        g.add_edge(Edge(4, 5, Decimal(5)))
        g.add_edge(Edge(5, 3, Decimal(6)))
        g.set_alias_node(2, 6)
        g.set_alias_node(3, 6)
        g.remove_edge(e1)
        g.remove_edge(e2)
        g.remove_edge(e3)
        r = [[0, 1], [1, 2], [2, 0]]
        self.assertEqual(select_start_node(g, r, -1), 3)

    def test_add_alias_connect(self):
        # 生成済みルートにエイリアスノードを追加
        g = AliasGraph()
        e1 = Edge(0, 1, Decimal(1))
        g.add_edge(e1)
        e2 = Edge(1, 2, Decimal(2))
        g.add_edge(e2)
        e3 = Edge(2, 0, Decimal(3))
        g.add_edge(e3)
        g.add_edge(Edge(3, 4, Decimal(4)))
        g.add_edge(Edge(4, 5, Decimal(5)))
        g.add_edge(Edge(5, 3, Decimal(6)))
        g.set_alias_node(2, 6)
        g.set_alias_node(3, 6)
        g.remove_edge(e1)
        g.remove_edge(e2)
        g.remove_edge(e3)
        r = [[0, 1], [1, 2], [2, 0]]
        add_alias_connect(r, 3, g)
        self.assertEqual(r, [[0, 1], [1, 2], [2, 3], [3, 2], [2, 0]])
