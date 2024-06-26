import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from test.support import captured_stdout
from decimal import Decimal
from edge import Edge
from alias_graph import AliasGraph
from eulerian_task import EulerianTask

class EulerianTaskTest(unittest.TestCase):
    def test_insert(self):
        # 要素を適切なソート位置まで移動する
        e_list = [('一', '一', Decimal(1)),
                  ('一', '二', Decimal(1)),
                  ('二', '一', Decimal(2)),
                  ('一', '一', Decimal(2)),
                  ('二', '二', Decimal(1)),
                  ('一', '二', Decimal(2)),
                  ]
        EulerianTask.insert(e_list, 3)
        exp = [('一', '一', Decimal(1)),
               ('一', '一', Decimal(2)),
               ('一', '二', Decimal(1)),
               ('二', '一', Decimal(2)),
               ('二', '二', Decimal(1)),
               ('一', '二', Decimal(2)),
               ]
        self.assertEqual(e_list, exp)

    def test_insert_0(self):
        # 要素を先頭まで移動する
        e_list = [('一', '一', Decimal(2)),
                  ('一', '二', Decimal(1)),
                  ('二', '一', Decimal(2)),
                  ('二', '二', Decimal(1)),
                  ('一', '一', Decimal(1)),
                  ('一', '二', Decimal(2)),
                  ]
        EulerianTask.insert(e_list, 4)
        exp = [('一', '一', Decimal(1)),
               ('一', '一', Decimal(2)),
               ('一', '二', Decimal(1)),
               ('二', '一', Decimal(2)),
               ('二', '二', Decimal(1)),
               ('一', '二', Decimal(2)),
               ]
        self.assertEqual(e_list, exp)

    def test_sort_edges(self):
        # エッジデータをソートする
        e_list = [('二', '二', Decimal(1)),
                  ('一', '一', Decimal(2)),
                  ('一', '二', Decimal(1)),
                  ('二', '一', Decimal(2)),
                  ('一', '一', Decimal(1)),
                  ('一', '二', Decimal(2)),
                  ]
        EulerianTask.sort_edges(e_list)
        exp = [('一', '一', Decimal(1)),
               ('一', '一', Decimal(2)),
               ('一', '二', Decimal(1)),
               ('一', '二', Decimal(2)),
               ('二', '一', Decimal(2)),
               ('二', '二', Decimal(1)),
               ]
        self.assertEqual(e_list, exp)

    def test_remove_added_edge_sg(self):
        # 始点と終点間に追加したエッジを削除する
        # [始点, 終点]のデータが中間にあるとき
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        start_point = '弐'
        goal_point = '参'
        route = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        exp = [[2, 1], [1, 0], [0, 6], [6, 5], [5, 4], [4, 3]]
        act = EulerianTask.remove_added_edge(start_point, goal_point, node_list, route)
        self.assertEqual(act, exp)

    def test_remove_added_edge_gs(self):
        # 始点と終点間に追加したエッジを削除する
        # [終点, 始点]のデータが中間にあるとき
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        start_point = '参'
        goal_point = '弐'
        route = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        exp = [[3, 4], [4, 5], [5, 6], [6, 0], [0, 1], [1, 2]]
        act = EulerianTask.remove_added_edge(start_point, goal_point, node_list, route)
        self.assertEqual(act, exp)

    def test_remove_added_edge_sg_0(self):
        # 始点と終点間に追加したエッジを削除する
        # [始点, 終点]のデータが最初にあるとき
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        start_point = '零'
        goal_point = '壱'
        route = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        exp = [[0, 6], [6, 5], [5, 4], [4, 3], [3, 2], [2, 1]]
        act = EulerianTask.remove_added_edge(start_point, goal_point, node_list, route)
        self.assertEqual(act, exp)

    def test_remove_added_edge_gs_0(self):
        # 始点と終点間に追加したエッジを削除する
        # [終点, 始点]のデータが最初にあるとき
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        start_point = '壱'
        goal_point = '零'
        route = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        exp = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        act = EulerianTask.remove_added_edge(start_point, goal_point, node_list, route)
        self.assertEqual(act, exp)

    def test_remove_added_edge_sg_l(self):
        # 始点と終点間に追加したエッジを削除する
        # [始点, 終点]のデータが最後にあるとき
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        start_point = '陸'
        goal_point = '零'
        route = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        exp = [[6, 5], [5, 4], [4, 3], [3, 2], [2, 1], [1, 0]]
        act = EulerianTask.remove_added_edge(start_point, goal_point, node_list, route)
        self.assertEqual(act, exp)

    def test_remove_added_edge_gs_l(self):
        # 始点と終点間に追加したエッジを削除する
        # [終点, 始点]のデータが最後にあるとき
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        start_point = '零'
        goal_point = '陸'
        route = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
        exp = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
        act = EulerianTask.remove_added_edge(start_point, goal_point, node_list, route)
        self.assertEqual(act, exp)

    def test_is_valid_node_name(self):
        # ノード名がリストにあるかを検索
        node_list = ['零', '壱', '弐', '参', '肆', '伍', '陸']
        self.assertTrue(EulerianTask.is_valid_node_name('零', node_list))
        self.assertFalse(EulerianTask.is_valid_node_name('佰', node_list))
        self.assertFalse(EulerianTask.is_valid_node_name('', node_list))
        self.assertFalse(EulerianTask.is_valid_node_name(None, node_list))

    def test_show_start_goal_vv(self):
        # 始点と終点の画面表示
        # 始点も終点も有効
        node_list = ['零', '壱']

        with captured_stdout() as stdout:
            EulerianTask.show_start_goal('零', '壱', node_list)
            outputs = stdout.getvalue().splitlines()
        self.assertEqual(outputs[0], '始点: 零  終点: 壱')

    def test_show_start_goal_vi(self):
        # 始点と終点の画面表示
        # 始点は有効、終点は無効
        node_list = ['零', '壱']

        with captured_stdout() as stdout:
            EulerianTask.show_start_goal('零', '弐', node_list)
            outputs = stdout.getvalue().splitlines()
        self.assertEqual(outputs[0], "始点: 零  '弐'が見つかりませんでした")

    def test_show_start_goal_iv(self):
        # 始点と終点の画面表示
        # 始点は無効、終点は有効
        node_list = ['零', '壱']

        with captured_stdout() as stdout:
            EulerianTask.show_start_goal('弐', '壱', node_list)
            outputs = stdout.getvalue().splitlines()
        self.assertEqual(outputs[0], "'弐'が見つかりませんでした")

    def test_show_start_goal_vn(self):
        # 始点と終点の画面表示
        # 始点は有効、終点は空文字
        node_list = ['零', '壱']

        with captured_stdout() as stdout:
            EulerianTask.show_start_goal('零', '', node_list)
            outputs = stdout.getvalue().splitlines()
        self.assertEqual(outputs[0], '始点: 零')

    def test_show_start_goal_nv(self):
        # 始点と終点の画面表示
        # 始点は空文字、終点は有効
        node_list = ['零', '壱']

        with captured_stdout() as stdout:
            EulerianTask.show_start_goal('', '壱', node_list)
            outputs = stdout.getvalue().splitlines()
        self.assertEqual(len(outputs), 0)

    def test_generate_edge_list(self):
        # グラフからエッジのリストを生成
        node_list = ['零', '壱', '弐', '参', '肆', '伍']
        graph = AliasGraph()
        graph.add_edge(Edge(0, 2, Decimal(1)))
        graph.add_edge(Edge(0, 5, Decimal(2)))
        graph.add_edge(Edge(1, 3, Decimal(3)))
        graph.add_edge(Edge(1, 4, Decimal(4)))
        graph.add_edge(Edge(1, 5, Decimal(5)))
        graph.add_edge(Edge(4, 5, Decimal(6)))
        act: list[tuple[str, str, Decimal]] = EulerianTask.generate_edge_list(graph, node_list)
        self.assertEqual(len(act), 6)
        self.assertTrue(('弐', '零', Decimal(1)) in act)
        self.assertTrue(('伍', '零', Decimal(2)) in act)
        self.assertTrue(('参', '壱', Decimal(3)) in act)
        self.assertTrue(('壱', '肆', Decimal(4)) in act)
        self.assertTrue(('伍', '壱', Decimal(5)) in act)
        self.assertTrue(('伍', '肆', Decimal(6)) in act)

    def test_generate_transfer_list(self):
        # グラフから同じとみなすノードのリストを生成
        node_list = ['零', '壱', '弐', '参', '肆']
        graph = AliasGraph()
        graph.add_edge(Edge(0, 1, Decimal(1)))
        graph.add_edge(Edge(1, 2, Decimal(2)))
        graph.add_edge(Edge(2, 3, Decimal(3)))
        graph.add_edge(Edge(3, 4, Decimal(4)))
        graph.set_alias_node(0, 10)
        graph.set_alias_node(1, 10)
        graph.set_alias_node(2, 11)
        graph.set_alias_node(3, 11)
        graph.set_alias_node(4, 11)
        act = EulerianTask.generate_transfer_list(graph, node_list)
        self.assertEqual(len(act), 4)
        self.assertTrue(('壱', '零') in act)
        self.assertTrue(('参', '弐') in act)
        self.assertTrue(('参', '肆') in act)
        self.assertTrue(('弐', '肆') in act)
