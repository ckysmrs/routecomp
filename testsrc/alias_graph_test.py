import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from edge import Edge
from alias_graph import AliasGraph

class AliasGraphTest(unittest.TestCase):
    def test_clear(self):
        # グラフを空にする
        sut = AliasGraph()
        self.assertEqual(sut.get_edge_size(), 0)

        e = Edge(0, 0, Decimal('1'))
        sut.add_edge(e)
        self.assertEqual(sut.get_edge_size(), 1)

        sut.clear()
        self.assertEqual(sut.get_edge_size(), 0)

    def test_clear_alias(self):
        # グラフを空にしたとき、エイリアス情報も消す
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal(1)))
        sut.add_edge(Edge(2, 3, Decimal(2)))
        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 10)
        self.assertTrue(sut.is_connected())

        sut.clear()
        sut.add_edge(Edge(0, 1, Decimal(1)))
        sut.add_edge(Edge(2, 3, Decimal(2)))
        self.assertFalse(sut.is_connected())

    def test_get_edge(self):
        # 指定した位置の辺を返す
        sut = AliasGraph()

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

    def test_get_edge_by_nodes(self):
        # 指定した頂点を結ぶ辺を返す
        sut = AliasGraph()

        e1 = Edge(0, 1, Decimal('10'))
        e2 = Edge(2, 3, Decimal('10'))
        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.set_alias_node(1, 4)
        sut.set_alias_node(2, 4)

        e = sut.get_edge_by_nodes(4, 0)
        self.assertIsNotNone(e)
        self.assertIs(e, e1)
        self.assertIsNone(sut.get_edge_by_nodes(0, 1))

    def test_get_edge_by_real_nodes(self):
        # 指定した頂点を結ぶ辺を返す
        sut = AliasGraph()

        e1 = Edge(0, 1, Decimal('10'))
        e2 = Edge(1, 2, Decimal('10'))
        sut.add_edge(e1)
        sut.add_edge(e2)

        e = sut.get_edge_by_real_nodes(1, 0)
        self.assertIsNotNone(e)
        self.assertIs(e, e1)
        self.assertIsNone(sut.get_edge_by_real_nodes(0, 2))

    def test_get_edge_list_by_node(self):
        # 指定した頂点に接続された辺のリストを返す
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(1, 2, Decimal('11')))
        sut.add_edge(Edge(0, 2, Decimal('12')))
        sut.add_edge(Edge(1, 3, Decimal('10')))
        sut.add_edge(Edge(4, 5, Decimal('10')))
        sut.set_alias_node(3, 6)
        sut.set_alias_node(4, 6)

        self.assertEqual(len(sut.get_edge_list_by_node(0)), 2)
        self.assertEqual(len(sut.get_edge_list_by_node(1)), 3)
        self.assertEqual(len(sut.get_edge_list_by_node(2)), 2)
        self.assertEqual(len(sut.get_edge_list_by_node(3)), 0)
        self.assertEqual(len(sut.get_edge_list_by_node(4)), 0)
        self.assertEqual(len(sut.get_edge_list_by_node(5)), 1)
        self.assertEqual(len(sut.get_edge_list_by_node(6)), 2)

    def test_get_edge_size(self):
        # 辺の数を返す
        sut = AliasGraph()

        self.assertEqual(sut.get_edge_size(), 0)

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e2)

        self.assertEqual(sut.get_edge_size(), 3)

    def test_get_node_size(self):
        # エイリアスの頂点の数を返す
        sut = AliasGraph()
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

    def test_get_real_node_size(self):
        # オリジナルとエイリアスの頂点の数を返す
        sut = AliasGraph()
        self.assertEqual(sut.get_real_node_size(), 0)

        sut.add_edge(Edge(0, 1, Decimal('1')))
        sut.add_edge(Edge(2, 3, Decimal('1')))
        sut.set_alias_node(1, 4)
        sut.set_alias_node(2, 4)
        self.assertEqual(sut.get_real_node_size(), 4)
        self.assertEqual(sut.get_node_size(), 3)

    def test_edge_generator(self):
        # エッジのジェネレータを返す
        sut = AliasGraph()

        e1 = Edge(0, 1, Decimal('0.1'))
        e2 = Edge(2, 3, Decimal('0.2'))
        sut.add_edge(e1)
        sut.add_edge(e2)
        exp = (e1, e2)

        for i, e in enumerate(sut.edge_generator()):
            self.assertEqual(e, exp[i])

    def test_add_none(self):
        # Noneの辺は追加しない
        sut = AliasGraph()
        self.assertEqual(sut.get_edge_size(), 0)

        sut.add_edge(None)
        self.assertEqual(sut.get_edge_size(), 0)

    def test_add_edge_with_clean_alias(self):
        # 新しいノードにはエイリアス情報が無い
        sut = AliasGraph()
        e1 = Edge(0, 1, Decimal(1))
        sut.add_edge(e1)
        e2 = Edge(2, 3, Decimal(2))
        sut.add_edge(e2)
        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 10)
        sut.remove_edge(e1)
        self.assertTrue(1 in sut.alias_map)
        sut.add_edge(e1)
        self.assertFalse(1 in sut.alias_map)

    def test_remove_edge(self):
        # 辺を削除する
        sut = AliasGraph()

        e1 = Edge(0, 0, Decimal('1'))
        e2 = Edge(0, 0, Decimal('1'))

        sut.add_edge(e1)
        sut.add_edge(e2)

        self.assertEqual(sut.get_edge_size(), 2)

        sut.remove_edge(e1)
        self.assertEqual(sut.get_edge_size(), 1)

        if sut.get_edge_size() == 1:
            self.assertIs(sut.get_edge(0), e2)

    def test_remove_alias_edge(self):
        # 必要なくなったエイリアスも削除する
        sut = AliasGraph()
        e1 = Edge(0, 1, Decimal('2'))
        sut.add_edge(e1)
        e2 = Edge(1, 2, Decimal('3'))
        sut.add_edge(e2)
        sut.set_alias_node(0, 3)
        self.assertTrue(sut.contains_node(0))
        self.assertTrue(sut.contains_node(1))
        self.assertTrue(sut.contains_node(2))
        self.assertTrue(sut.contains_node(3))

        sut.remove_edge(e1)
        self.assertFalse(sut.contains_node(0))
        self.assertTrue(sut.contains_node(1))
        self.assertTrue(sut.contains_node(2))
        self.assertFalse(sut.contains_node(3))

    def test_remove_edge_keep_alias_info(self):
        # ノードが無くなってもエイリアス情報は保持する
        sut = AliasGraph()
        e1 = Edge(0, 1, Decimal(1))
        sut.add_edge(e1)
        e2 = Edge(2, 3, Decimal(2))
        sut.add_edge(e2)
        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 10)
        self.assertTrue(1 in sut.alias_map)

        sut.remove_edge(e1)
        self.assertTrue(1 in sut.alias_map)

    def test_get_copy_of_nodes(self):
        # ノード一覧を返す
        sut = AliasGraph()
        sut.add_edge(Edge(2, 3, Decimal('1')))
        sut.add_edge(Edge(5, 7, Decimal('1')))
        sut.add_edge(Edge(11, 13, Decimal('1')))
        sut.set_alias_node(2, 17)
        sut.set_alias_node(7, 17)
        act = sut.get_copy_of_nodes()
        self.assertEqual(act, {3, 5, 11, 13, 17})

    def test_equals_and_hash(self):
        # equalsがTrueのときは同じハッシュコードを返す
        g1 = AliasGraph()
        g2 = AliasGraph()

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
        g1 = AliasGraph()
        g2 = AliasGraph()

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

    def test_equals_alias(self):
        # エイリアスが異なるグラフは同じとみなさない
        g1 = AliasGraph()
        g2 = AliasGraph()

        g1.add_edge(Edge(0, 1, Decimal('1')))
        g1.add_edge(Edge(2, 3, Decimal('1')))
        g2.add_edge(Edge(0, 1, Decimal('1')))
        g2.add_edge(Edge(2, 3, Decimal('1')))
        g2.set_alias_node(1, 4)
        g2.set_alias_node(2, 4)

        self.assertFalse(g1 == g2)

    def test_equals_instance(self):
        # 同じインスタンスのequalsはTrueを返す
        sut = AliasGraph()

        self.assertTrue(sut == sut)

    def test_copy_instance(self):
        # AliasGraphクラスのコピーを生成する
        g = AliasGraph()

        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 2, Decimal('11'))

        g.add_edge(e1)
        g.add_edge(e2)

        sut = AliasGraph.copy_instance(g)

        self.assertIsNot(sut, g)
        self.assertEqual(sut, g)

    def test_copy_instance_alias(self):
        # エイリアス付きグラフのコピーを生成する
        g = AliasGraph()

        g.add_edge(Edge(0, 1, Decimal('10')))
        g.add_edge(Edge(2, 3, Decimal('11')))
        g.add_edge(Edge(4, 5, Decimal('12')))
        g.set_alias_node(1, 10)
        g.set_alias_node(2, 10)
        sut = AliasGraph.copy_instance(g)
        sut.set_alias_node(3, 20)
        sut.set_alias_node(4, 20)

        self.assertEqual(g.get_alias_node(0),  0)
        self.assertEqual(g.get_alias_node(1), 10)
        self.assertEqual(g.get_alias_node(2), 10)
        self.assertEqual(g.get_alias_node(3),  3)
        self.assertEqual(g.get_alias_node(4),  4)
        self.assertEqual(g.get_alias_node(5),  5)

        self.assertEqual(sut.get_alias_node(0),  0)
        self.assertEqual(sut.get_alias_node(1), 10)
        self.assertEqual(sut.get_alias_node(2), 10)
        self.assertEqual(sut.get_alias_node(3), 20)
        self.assertEqual(sut.get_alias_node(4), 20)
        self.assertEqual(sut.get_alias_node(5),  5)

    def test_contains_graph(self):
        # グラフを含んでいるかを判定する
        sut = AliasGraph()
        g   = AliasGraph()

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
        sut = AliasGraph()
        self.assertEqual(sut.get_total_cost(), 0)

        e1 = Edge(0, 0, Decimal('2'))
        sut.add_edge(e1)
        self.assertEqual(sut.get_total_cost(), 2)

        e2 = Edge(0, 0, Decimal('3'))
        sut.add_edge(e2)
        self.assertEqual(sut.get_total_cost(), 5)

    def test_contains_node(self):
        # 指定の頂点を含んでいるかを返す
        sut = AliasGraph()

        sut.add_edge(Edge(0, 1, Decimal('1')))
        sut.set_alias_node(0, 2)

        self.assertTrue(sut.contains_node(0))
        self.assertTrue(sut.contains_node(1))
        self.assertTrue(sut.contains_node(2))
        self.assertFalse(sut.contains_node(3))

    def test_contains_edge(self):
        # 指定の辺を含んでいるかを返す
        sut = AliasGraph()

        e1 = Edge(0, 1, Decimal('10'))
        e2 = Edge(0, 1, Decimal('10'))
        e3 = Edge(0, 1, Decimal('11'))
        sut.add_edge(e1)

        self.assertTrue(sut.contains_edge(e2))
        self.assertFalse(sut.contains_edge(e3))

    def test_merge_graph(self):
        # グラフをマージする
        sut = AliasGraph()
        g   = AliasGraph()

        sut.add_edge(Edge(0, 1, Decimal('1')))
        sut.set_alias_node(1, 6)
        g.add_edge(Edge(2, 3, Decimal('1')))
        g.add_edge(Edge(4, 5, Decimal('1')))
        g.set_alias_node(2, 6)
        g.set_alias_node(3, 7)
        g.set_alias_node(4, 7)

        self.assertEqual(sut.get_edge_size(), 1)

        sut.merge_graph(g)
        self.assertEqual(sut.get_edge_size(), 3)

        self.assertTrue(sut.contains_node(2))
        self.assertTrue(sut.contains_node(3))
        self.assertTrue(sut.contains_node(6))
        self.assertTrue(sut.contains_node(7))

    def test_merge_graph_diff_alias(self):
        # 同じノードに違うエイリアスが設定されているグラフを
        # マージすると例外を出す
        sut = AliasGraph()
        g   = AliasGraph()

        sut.add_edge(Edge(0, 1, Decimal('1')))
        sut.set_alias_node(1, 3)
        g.add_edge(Edge(1, 2, Decimal('1')))
        g.set_alias_node(1, 4)

        self.assertEqual(sut.get_edge_size(), 1)

        with self.assertRaises(ValueError):
            sut.merge_graph(g)

    def test_is_connected(self):
        # グラフが連結グラフかを調べる
        sut = AliasGraph()
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

    def test_is_connected_alias(self):
        # エイリアスグラフが連結グラフかを調べる
        sut = AliasGraph()

        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(2, 3, Decimal('10')))

        self.assertFalse(sut.is_connected())

        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 10)

        self.assertTrue(sut.is_connected())

    def test_is_connected_loop(self):
        # 円環グラフが連結グラフかを調べる
        sut = AliasGraph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(1, 2, Decimal('10'))
        e3  = Edge(2, 0, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)
        sut.add_edge(e3)

        self.assertTrue(sut.is_connected())

    def test_is_connected_loop_plus(self):
        # ループの後に追加の辺を付けたグラフが連結グラフかを調べる
        sut = AliasGraph()
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
        sut = AliasGraph()
        e1  = Edge(0, 1, Decimal('10'))
        e2  = Edge(0, 1, Decimal('10'))

        sut.add_edge(e1)
        sut.add_edge(e2)

        self.assertTrue(sut.is_connected())

    def test_empty_connected(self):
        # 空グラフを連結グラフと判定しない
        sut = AliasGraph()
        self.assertFalse(sut.is_connected())

    def test_is_euler_graph(self):
        # グラフがオイラーグラフかを調べる
        sut = AliasGraph()
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

    def test_is_euler_graph_alias(self):
        # グラフがオイラーグラフかを調べる
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(1, 2, Decimal('10')))
        sut.add_edge(Edge(2, 0, Decimal('10')))
        sut.add_edge(Edge(3, 4, Decimal('10')))
        sut.add_edge(Edge(4, 5, Decimal('10')))
        sut.add_edge(Edge(5, 3, Decimal('10')))
        self.assertFalse(sut.is_euler_graph())

        sut.set_alias_node(0, 3)
        self.assertTrue(sut.is_euler_graph())

    def test_number_of_edge(self):
        # ある辺が何本含まれているかを返す
        sut = AliasGraph()
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
        graph = AliasGraph()
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

    def test_pick_up_branch_and_remove_alias(self):
        # エイリアスを介した2本の枝線を取り出す
        graph = AliasGraph()
        graph.add_edge(Edge(0, 1, Decimal('1')))
        graph.add_edge(Edge(1, 2, Decimal('1')))
        graph.add_edge(Edge(0, 2, Decimal('1')))
        graph.add_edge(Edge(3, 4, Decimal('1')))
        graph.add_edge(Edge(5, 6, Decimal('1')))
        graph.set_alias_node(0, 10)
        graph.set_alias_node(3, 10)
        graph.set_alias_node(1, 11)
        graph.set_alias_node(5, 11)

        self.assertEqual(graph.get_node_size(), 5)
        self.assertEqual(graph.get_real_node_size(), 7)

        branch_graph = graph.pick_up_branch_and_remove()

        self.assertEqual(graph.get_node_size(), 3)
        self.assertEqual(graph.get_real_node_size(), 3)
        self.assertEqual(graph.get_edge_size(), 3)
        self.assertEqual(branch_graph.get_edge_size(), 2)
        self.assertTrue(branch_graph.contains_node(3))
        self.assertTrue(branch_graph.contains_node(6))
        self.assertEqual(graph.get_alias_node(0), 10)
        self.assertEqual(graph.get_alias_node(1), 11)
        self.assertEqual(branch_graph.get_alias_node(3), 10)
        self.assertEqual(branch_graph.get_alias_node(5), 11)

    def test_degree_map(self):
        # ノードの次数マップを返す
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(1, 2, Decimal('11')))
        sut.add_edge(Edge(0, 2, Decimal('12')))
        sut.add_edge(Edge(1, 3, Decimal('10')))
        sut.add_edge(Edge(4, 5, Decimal('10')))
        sut.add_edge(Edge(3, 5, Decimal('10')))
        sut.set_alias_node(2, 6)
        sut.set_alias_node(4, 6)
        sut.set_alias_node(3, 7)
        sut.set_alias_node(5, 7)

        degree_map: dict[int, int] = sut.get_degree_map()
        self.assertEqual(len(degree_map), 4)
        self.assertEqual(degree_map[0], 2)
        self.assertEqual(degree_map[1], 3)
        self.assertFalse(2 in degree_map)
        self.assertFalse(3 in degree_map)
        self.assertFalse(4 in degree_map)
        self.assertFalse(5 in degree_map)
        self.assertEqual(degree_map[6], 3)
        self.assertEqual(degree_map[7], 4)

    def test_get_real_node_from_node(self):
        # 指定ノードにつながったノードを1つ返す
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(2, 3, Decimal('11')))
        sut.set_alias_node(1, 4)
        sut.set_alias_node(2, 4)

        node = sut.get_real_node_from_node(4)
        self.assertTrue(node == 0 or node == 3)
    
    def test_get_alias_node(self):
        # ノードのエイリアスを返す
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(2, 3, Decimal('11')))
        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 10)
        self.assertEqual(sut.get_alias_node(0), 0)
        self.assertEqual(sut.get_alias_node(1), 10)
        self.assertEqual(sut.get_alias_node(2), 10)
        self.assertEqual(sut.get_alias_node(3), 3)

    def test_set_alias_node(self):
        # ノードにエイリアスを設定する
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('10')))
        sut.add_edge(Edge(2, 3, Decimal('11')))
        self.assertEqual(sut.get_node_size(), 4)
        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 10)
        edge_list = sut.get_edge_list_by_node(10)
        self.assertEqual(len(edge_list), 2)
        self.assertEqual(sut.get_node_size(), 3)

    def test_is_same(self):
        edges1 = []
        edges1.append(Edge(0, 1, Decimal('10')))
        edges2 = []
        edges2.append(Edge(0, 1, Decimal('10')))
        self.assertTrue(AliasGraph.is_same(edges1, edges2))

    def test_is_not_same(self):
        edges1 = []
        edges1.append(Edge(0, 1, Decimal('10')))
        edges2 = []
        edges2.append(Edge(0, 1, Decimal('10')))
        edges2.append(Edge(2, 3, Decimal('11')))
        self.assertFalse(AliasGraph.is_same(edges1, edges2))

    def test_get_alias_dict(self):
        # エイリアスの辞書を返す
        sut = AliasGraph()
        sut.add_edge(Edge(0, 1, Decimal('1')))
        sut.add_edge(Edge(2, 3, Decimal('1')))
        sut.add_edge(Edge(4, 5, Decimal('1')))
        sut.set_alias_node(0, 10)
        sut.set_alias_node(1, 10)
        sut.set_alias_node(2, 11)
        sut.set_alias_node(3, 11)
        sut.set_alias_node(4, 11)
        act = sut.get_alias_dict()
        self.assertEqual(act[10], {0, 1})
        self.assertEqual(act[11], {2, 3, 4})
