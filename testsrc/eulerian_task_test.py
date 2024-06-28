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
