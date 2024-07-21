import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from matching_graph import MatchingGraph

class MatchingGraphTest(unittest.TestCase):
    def test_add_edge(self):
        # 辺を登録する
        sut = MatchingGraph(3)
        sut.add_edge(1, 2)
        self.assertEqual(sut.get_num_edges(), 1)
        self.assertEqual(sut.get_edge_index(2, 1), 0)

    def test_init_with_edges(self):
        # 辺を初期値に指定する
        sut = MatchingGraph(4, [(0, 1), (3, 2)])
        self.assertEqual(sut.get_num_edges(), 2)
        i0 = sut.get_edge_index(1, 0)
        e0 = sut.get_edge(i0)
        self.assertTrue(e0 == (0, 1) or e0 == (1, 0))
        i1 = sut.get_edge_index(2, 3)
        e1 = sut.get_edge(i1)
        self.assertTrue(e1 == (2, 3) or e1 == (3, 2))

    def test_add_vertex(self):
        # 頂点を追加する
        sut = MatchingGraph(2)
        self.assertEqual(sut.get_num_vertices(), 2)
        sut.add_vertex()
        self.assertEqual(sut.get_num_vertices(), 3)

    def test_invalid_edge_index(self):
        # 辺の不正なインデックスには例外を出す
        sut = MatchingGraph()
        with self.assertRaises(IndexError, msg='Error: edge does not exist'):
            sut.get_edge(1)

    def test_edge_with_invalid_node_index(self):
        # 不正なノードの辺指定は例外を出す
        sut = MatchingGraph(3)
        with self.assertRaises(IndexError, msg='Error: vertex does not exist'):
            sut.get_edge_index(2, 3)

    def test_nonexistent_edge(self):
        # 辺が存在しないノード指定は例外を出す
        sut = MatchingGraph(2)
        with self.assertRaises(IndexError, msg='Error: edge does not exist'):
            sut.get_edge_index(0, 1)

    def test_add_edge_to_nonexistent_node(self):
        # 存在しないノードに辺を追加すると例外を出す
        sut = MatchingGraph(2)
        with self.assertRaises(IndexError, msg='Error: vertex does not exist'):
            sut.add_edge(1, 2)

    def test_add_edge_twice(self):
        # 辺を上書きしても何もしない
        sut = MatchingGraph(2)
        sut.add_edge(0, 1)
        self.assertEqual(sut.get_num_edges(), 1)
        sut.add_edge(1, 0)
        self.assertEqual(sut.get_num_edges(), 1)

    def test_adj_node(self):
        # 隣接ノードリストを返す
        sut = MatchingGraph(3)
        sut.add_edge(0, 1)
        sut.add_edge(1, 2)
        act = sut.get_adj_list(1)
        self.assertEqual(len(act), 2)
        self.assertEqual(set(act), {0, 2})

    def test_adj_node_of_nonexistent_node(self):
        # 存在しないノードの隣接ノード取得は例外を出す
        sut = MatchingGraph(2)
        with self.assertRaises(IndexError, msg='Error: vertex does not exist'):
            sut.get_adj_list(2)

    def test_adj_mat(self):
        # 隣接マトリックス返す
        sut = MatchingGraph(4)
        sut.add_edge(0, 1)
        sut.add_edge(0, 2)
        sut.add_edge(0, 3)
        sut.add_edge(1, 3)
        exp = [[False, True, True, True],
               [True, False, False, True],
               [True, False, False, False],
               [True, True, False, False],]
        self.assertEqual(sut.get_adj_mat(), exp)

    def test_init(self):
        # コンストラクタを3回(複数回)呼ぶ
        # デフォルト引数値をリストにした動作の確認
        sut = MatchingGraph(3, [(0, 1)])
        self.assertEqual(sut.get_num_vertices(), 3)
        self.assertEqual(sut.get_num_edges(), 1)
        sut = MatchingGraph(3, [(0, 2), (1, 2)])
        self.assertEqual(sut.get_num_vertices(), 3)
        self.assertEqual(sut.get_num_edges(), 2)
        sut = MatchingGraph(3)
        self.assertEqual(sut.get_num_vertices(), 3)
        self.assertEqual(sut.get_num_edges(), 0)
