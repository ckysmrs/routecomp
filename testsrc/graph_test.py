import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from edge import Edge
from graph import Graph

class GraphTest(unittest.TestCase):
    def test_clear(self):
        # グラフを空にする
        sut = Graph()
        self.assertEqual(sut.get_edge_size(), 0)

        e = Edge(0, 0, Decimal('1'))
        sut.add_edge(e)
        self.assertEqual(sut.get_edge_size(), 1)

        sut.clear()
        self.assertEqual(sut.get_edge_size(), 0)

    def test_get_edge(self):
        # 指定した位置の辺を返す
        sut = Graph()

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))
        e3 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e1)
        sut.add_edge(e3)
        sut.add_edge(e2)
        sut.add_edge(e3)

        self.assertIs(sut.get_edge(2), e1)
        self.assertIs(sut.get_edge(3), e3)
        self.assertIs(sut.get_edge(4), e2)

    def test_get_edge_by_real_nodes(self):
        # 指定した頂点を結ぶ辺を返す
        sut = Graph()

        e1 = Edge(0, 1, Decimal('10'))
        e2 = Edge(1, 2, Decimal('10'))
        sut.add_edge(e1)
        sut.add_edge(e2)

        e = sut.get_edge_by_nodes(1, 0)
        self.assertIsNotNone(e)
        self.assertIs(e, e1)
        self.assertIsNone(sut.get_edge_by_nodes(0, 2))

    def test_get_edge_list_by_node(self):
        # 指定した頂点に接続された辺のリストを返す
        sut = Graph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(1, 2, Decimal('11')))
        sut.add_edge(Edge(0, 2, Decimal('12')))
        sut.add_edge(Edge(1, 3, Decimal('10')))

        self.assertEqual(len(sut.get_edge_list_by_node(0)), 2)
        self.assertEqual(len(sut.get_edge_list_by_node(1)), 3)
        self.assertEqual(len(sut.get_edge_list_by_node(2)), 2)
        self.assertEqual(len(sut.get_edge_list_by_node(3)), 1)

    def test_get_edge_size(self):
        # 辺の数を返す
        sut = Graph()

        self.assertEqual(sut.get_edge_size(), 0)

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e2)

        self.assertEqual(sut.get_edge_size(), 3)

    def test_get_node_size(self):
        # 頂点の数を返す
        sut = Graph()
        self.assertEqual(sut.get_node_size(), 0)

        e1 = Edge(0, 1, Decimal('1'))
        sut.add_edge(e1)
        self.assertEqual(sut.get_node_size(), 2)

        e2 = Edge(2, 3, Decimal('1'))
        sut.add_edge(e2)
        self.assertEqual(sut.get_node_size(), 4)

        e3 = Edge(1, 4, Decimal('1'))
        sut.add_edge(e3)
        self.assertEqual(sut.get_node_size(), 5)

    def test_iterator(self):
        # 辺を追加して辺のリストを取得する
        sut = Graph()

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        sut.add_edge(e2)

        self.assertEqual(sut.get_edge_size(), 2)

        if sut.get_edge_size() == 2:
            ite_edge = sut.edge_iterator()
            self.assertIs(next(ite_edge), e1)
            self.assertIs(next(ite_edge), e2)

    def test_add_none(self):
        # Noneの辺は追加しない
        sut = Graph()
        self.assertEqual(sut.get_edge_size(), 0)

        sut.add_edge(None)
        self.assertEqual(sut.get_edge_size(), 0)

    def test_remove_edge(self):
        # 辺を削除する
        sut = Graph()

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        sut.add_edge(e2)

        self.assertEqual(sut.get_edge_size(), 2)

        sut.remove_edge(e1)
        self.assertEqual(sut.get_edge_size(), 1)

        if sut.get_edge_size() == 1:
            self.assertIs(sut.get_edge(0), e2)

    def test_get_copy_of_nodes(self):
        # ノード一覧を返す
        sut = Graph()
        sut.add_edge(Edge(2, 3, Decimal('1')))
        sut.add_edge(Edge(5, 7, Decimal('1')))
        sut.add_edge(Edge(11, 13, Decimal('1')))
        act = sut.get_copy_of_nodes()
        self.assertEqual(act, {2, 3, 5, 7, 11, 13})

    def test_equals_and_hash(self):
        # equalsがTrueのときは同じハッシュ値を返す
        g1 = Graph()
        g2 = Graph()

        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 2, Decimal('11'))

        g1.add_edge(e1)
        g1.add_edge(e2)

        g2.add_edge(e2)
        g2.add_edge(e1)
        self.assertTrue(g1 == g2)
        self.assertEqual(hash(g1), hash(g2))

    def test_equals_by_edge(self):
        # 辺のリストが同じときは同じグラフとみなす
        g1 = Graph()
        g2 = Graph()

        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 2, Decimal('11'))
        e3 = Edge(1, 3, Decimal('10'))

        g1.add_edge(e1)
        g1.add_edge(e2)
        g1.add_edge(e3)

        self.assertFalse(g1 == g2)

        g2.add_edge(e2)
        g2.add_edge(e3)
        g2.add_edge(e1)
        self.assertTrue(g1 == g2)

    def test_equals_instance(self):
        # 同じインスタンスのequalsはtrueを返す
        sut = Graph()

        self.assertTrue(sut == sut)

    def test_not_equals_other(self):
        # 異なるクラスとのequalsはFalseを返す
        sut = Graph()

        self.assertFalse(sut == 0)

    def test_copy(self):
        # Graphクラスのコピーを生成する
        g = Graph()

        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 2, Decimal('11'))

        g.add_edge(e1)
        g.add_edge(e2)

        sut = Graph.copy_instance(g)

        self.assertIsNot(sut, g)
        self.assertEqual(sut, g)

    def test_contains_graph(self):
        # グラフを含んでいるかを判定する
        sut = Graph()
        g   = Graph()

        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 2, Decimal('11'))
        e3 = Edge(1, 3, Decimal('10'))
        e4 = Edge(2, 3, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e3)
        self.assertTrue(sut.contains_graph(g))

        g.add_edge(e2)
        self.assertTrue(sut.contains_graph(g))

        g.add_edge(e4)
        self.assertFalse(sut.contains_graph(g))

    def test_total_cost(self):
        # 総コストを返す
        sut = Graph()
        self.assertEqual(sut.get_total_cost(), 0)

        e1 = Edge(0, 0, Decimal('2'))
        sut.add_edge(e1)
        self.assertEqual(sut.get_total_cost(), 2)

        e2 = Edge(0, 0, Decimal('3'))
        sut.add_edge(e2)
        self.assertEqual(sut.get_total_cost(), 5)

    def test_get_adjacent_node(self):
        # 隣接ノードを返す
        sut = Graph()
        sut.add_edge(Edge(0, 1, Decimal(1)))
        self.assertEqual(sut.get_node_from_node(0), 1)

    def test_get_adjacent_node_not_exist(self):
        # 存在しないノードにつながるノード
        sut = Graph()
        sut.add_edge(Edge(0, 1, Decimal(1)))
        self.assertIsNone(sut.get_node_from_node(2))

    def test_contains_node(self):
        # 指定の頂点を含んでいるかを返す
        sut = Graph()

        edge = Edge(0, 1, Decimal('1'))
        sut.add_edge(edge)

        self.assertTrue(sut.contains_node(0))
        self.assertFalse(sut.contains_node(2))

    def test_contains_edge(self):
        # 指定の辺を含んでいるかを返す
        sut = Graph()

        e1 = Edge(0, 1, Decimal('10'))
        e2 = Edge(0, 1, Decimal('10'))
        e3 = Edge(0, 1, Decimal('11'))
        sut.add_edge(e1)

        self.assertTrue(sut.contains_edge(e2))
        self.assertFalse(sut.contains_edge(e3))

    def test_merge_graph(self):
        # グラフをマージする
        sut = Graph()
        g   = Graph()

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))
        e3 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        g.add_edge(e2)
        g.add_edge(e3)
        self.assertEqual(sut.get_edge_size(), 1)

        sut.merge_graph(g)
        self.assertEqual(sut.get_edge_size(), 3)

        self.assertTrue(sut.contains_edge(e2))
        self.assertTrue(sut.contains_edge(e3))

    def test_is_connected(self):
        # グラフが連結グラフかを調べる
        sut = Graph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(1, 2, Decimal('10'))
        e4  = Edge(1, 3, Decimal('10'))
        e7  = Edge(2, 4, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e4)
        sut.add_edge(e7)

        self.assertFalse(sut.is_connected())

        sut.add_edge(e2)

        self.assertTrue(sut.is_connected())

    def test_is_connected_loop(self):
        # 円環グラフが連結グラフかを調べる
        sut = Graph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(1, 2, Decimal('10'))
        e3  = Edge(2, 0, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e3)

        self.assertTrue(sut.is_connected())

    def test_is_connected_loop_plus(self):
        # ループの後に追加の辺を付けたグラフが連結グラフかを調べる
        sut = Graph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(1, 2, Decimal('10'))
        e3  = Edge(2, 0, Decimal('10'))
        e4  = Edge(1, 3, Decimal('10'))

        # アルゴリズムを確認するため、以下の順序で辺を追加
        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e3)
        sut.add_edge(e4)

        self.assertTrue(sut.is_connected())

    def test_is_connected_double(self):
        # 2重辺が連結グラフかを調べる
        sut = Graph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(0, 1, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)

        self.assertTrue(sut.is_connected())

    def test_empty_connected(self):
        # 空グラフを連結グラフと判定しない
        sut = Graph()
        self.assertFalse(sut.is_connected())

    def test_is_euler_graph(self):
        # グラフがオイラーグラフかを調べる
        sut = Graph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(1, 2, Decimal('10'))
        e3  = Edge(0, 2, Decimal('10'))
        e4  = Edge(1, 3, Decimal('10'))
        e5  = Edge(2, 3, Decimal('10'))
        e6  = Edge(1, 4, Decimal('10'))
        e7  = Edge(2, 4, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e3)
        sut.add_edge(e4)
        sut.add_edge(e5)

        self.assertFalse(sut.is_euler_graph())

        sut.add_edge(e6)
        sut.add_edge(e7)

        self.assertTrue(sut.is_euler_graph())

    def test_is_euler_graph_disconnect(self):
        # 非連結グラフがオイラーグラフかを調べる
        sut = Graph()

        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(1, 0, Decimal('10')))
        sut.add_edge(Edge(2, 3, Decimal('10')))
        sut.add_edge(Edge(3, 2, Decimal('10')))

        self.assertFalse(sut.is_euler_graph())

    def test_empty_euler(self):
        # 空グラフをオイラーグラフと判定しない
        sut = Graph()
        self.assertFalse(sut.is_euler_graph())

    def test_number_of_edge(self):
        # ある辺が何本含まれているかを返す
        sut = Graph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(1, 2, Decimal('11'))
        e3  = Edge(0, 2, Decimal('12'))
        e4  = Edge(1, 3, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e3)
        sut.add_edge(e2)
        sut.add_edge(e3)
        sut.add_edge(e3)

        self.assertEqual(sut.get_number_of_edge(e1), 1)
        self.assertEqual(sut.get_number_of_edge(e2), 2)
        self.assertEqual(sut.get_number_of_edge(e3), 3)
        self.assertEqual(sut.get_number_of_edge(e4), 0)

    def test_branch(self):
        # 枝線を取り出す
        graph = Graph()
        graph.add_edge(Edge(0, 1, Decimal('10')))
        graph.add_edge(Edge(1, 2, Decimal('11')))
        graph.add_edge(Edge(0, 2, Decimal('12')))
        graph.add_edge(Edge(1, 3, Decimal('13')))

        self.assertEqual(graph.get_node_size(), 4)

        branch_graph = graph.pick_up_branch_and_remove()

        self.assertEqual(graph.get_node_size(), 3)
        self.assertEqual(graph.get_edge_size(), 3)
        self.assertEqual(branch_graph.get_edge_size(), 1)
        self.assertTrue(branch_graph.contains_node(3))

    def test_degree_map(self):
        # ノードの次数マップを返す
        sut = Graph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(1, 2, Decimal('11')))
        sut.add_edge(Edge(0, 2, Decimal('12')))
        sut.add_edge(Edge(1, 3, Decimal('10')))

        degree_map: dict[int, int] = sut.get_degree_map()
        self.assertEqual(len(degree_map), 4)
        self.assertEqual(degree_map[0], 2)
        self.assertEqual(degree_map[1], 3)
        self.assertEqual(degree_map[2], 2)
        self.assertEqual(degree_map[3], 1)

    def test_is_same(self):
        # 同じ辺のリストの比較
        edges1 = []
        edges1.append(Edge(0, 1, Decimal('10')))
        edges2 = []
        edges2.append(Edge(0, 1, Decimal('10')))
        self.assertTrue(Graph.is_same(edges1, edges2))

    def test_is_not_same(self):
        # 要素数が同じで内容が異なる辺のリストの比較
        edges1 = []
        edges1.append(Edge(0, 1, Decimal('10')))
        edges2 = []
        edges2.append(Edge(2, 3, Decimal('11')))
        self.assertFalse(Graph.is_same(edges1, edges2))

    def test_is_not_same_num_diff(self):
        # 要素数が異なる辺のリストの比較
        edges1 = []
        edges1.append(Edge(0, 1, Decimal('10')))
        edges2 = []
        edges2.append(Edge(0, 1, Decimal('10')))
        edges2.append(Edge(2, 3, Decimal('11')))
        self.assertFalse(Graph.is_same(edges1, edges2))
