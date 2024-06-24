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

    def test_refresh_transfer(self):
        # 乗り換えデータを整理する
        l: list[set[int]] = []
        l.append({0, 1})
        l.append({2, 3})
        l.append({0, 4})
        self.assertEqual(len(l), 3)
        graph_file_loader.refresh_transfer(l)
        self.assertEqual(len(l), 2)
        self.assertEqual(l[0], {0, 1, 4})
        self.assertEqual(l[1], {2, 3})
 
    def test_refresh_transfer_0(self):
        # 乗り換えデータを整理する
        # 1巡目ではマージされない場合
        l: list[set[int]] = []
        l.append({0, 1})
        l.append({2, 3})
        l.append({3, 4})
        self.assertEqual(len(l), 3)
        graph_file_loader.refresh_transfer(l)
        self.assertEqual(len(l), 2)
        self.assertEqual(l[0], {0, 1})
        self.assertEqual(l[1], {2, 3, 4})
 
    def test_refresh_transfer_num2(self):
        # 乗り換えデータを整理する
        # データが2個でマージされる場合
        l: list[set[int]] = []
        l.append({0, 1})
        l.append({0, 2})
        self.assertEqual(len(l), 2)
        graph_file_loader.refresh_transfer(l)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0], {0, 1, 2})
