import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
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
