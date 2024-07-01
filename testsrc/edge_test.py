import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from edge import Edge

class EdgeTest(unittest.TestCase):
    def test_minus_node1(self):
        # マイナスのノード1は設定できない
        with self.assertRaises(ValueError):
            Edge(-1, 2, Decimal('10'))

    def test_minus_node2(self):
        # マイナスのノード2は設定できない
        with self.assertRaises(ValueError):
            Edge(1, -2, Decimal('10'))

    def test_float_node1(self):
        # 小数のノード1は設定できない
        with self.assertRaises(ValueError):
            Edge(1.0, 2, Decimal('10'))

    def test_float_node2(self):
        # 小数のノード2は設定できない
        with self.assertRaises(ValueError):
            Edge(1, 2.0, Decimal('10'))

    def test_get_paired_node(self):
        # 指定ノードの反対側のノードを返す
        sut = Edge(1, 2, Decimal('10'))

        self.assertEqual(2, sut.get_paired_node(1))
        self.assertEqual(1, sut.get_paired_node(2))
        self.assertIsNone(sut.get_paired_node(3))

    def test_hash(self):
        # equalsがTrueのときは同じハッシュコードを返す
        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 2, Decimal('10'))

        self.assertTrue(e1 == e2)
        self.assertEqual(hash(e1), hash(e2))

    def test_hash_opp(self):
        # equalsがTrueのときは同じハッシュコードを返す
        # ノードが逆
        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(2, 1, Decimal('10'))

        self.assertTrue(e1 == e2)
        self.assertEqual(hash(e1), hash(e2))

    def test_equals_value(self):
        # 同じ内容の辺を同じ辺とみなす
        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(2, 1, Decimal('10'))

        self.assertTrue(e1 == e2)

        e3 = Edge(1, 2, Decimal('11'))
        self.assertFalse(e1 == e3)

        e4 = Edge(1, 2, Decimal('10'))
        self.assertTrue(e1 == e4)

    def test_equals_instance(self):
        # 同じインスタンスのequalsはTrueを返す
        sut = Edge(0, 0, Decimal('10'))

        self.assertTrue(sut == sut)

    def test_not_equal(self):
        # ノードが異なるときequalsはFalseを返す
        e1 = Edge(1, 2, Decimal('10'))
        e2 = Edge(1, 3, Decimal('10'))
        self.assertFalse(e1 == e2)

    def test_equals_none(self):
        # NoneとのequalsはFalseを返す
        sut = Edge(0, 0, Decimal('10'))

        self.assertFalse(sut == None)

    def test_eq_diff_inst(self):
        # 異なるクラスはFalseを返す
        a = Edge(0, 0, Decimal('10'))
        b = Decimal('0')
        self.assertFalse(a == b)

    def test_new_instance(self):
        # 頂点とコストを指定してインスタンスを生成する
        sut = Edge(0, 1, Decimal('2'))
        self.assertEqual(0, sut.get_node1())
        self.assertEqual(1, sut.get_node2())
        self.assertEqual(2, sut.get_cost())

        with self.assertRaises(ValueError):
            sut = Edge(0, -1, Decimal('2'))

        with self.assertRaises(ValueError):
            sut = Edge(0, 1, Decimal('-1'))

    def test_contains_node(self):
        # 頂点を含んでいるかを返す
        sut = Edge(0, 1, Decimal('10'))

        self.assertTrue(sut.contains_node(0))
        self.assertTrue(sut.contains_node(1))
        self.assertFalse(sut.contains_node(2))

    def test_contains_nodes(self):
        # 両方の頂点を含んでいるかを返す
        sut = Edge(0, 1, Decimal('10'))

        self.assertTrue(sut.contains_nodes(0, 1))
        self.assertTrue(sut.contains_nodes(1, 0))
        self.assertFalse(sut.contains_nodes(0, 2))
        self.assertFalse(sut.contains_nodes(2, 1))
        self.assertFalse(sut.contains_nodes(2, 3))

    def test_str(self):
        # __str__の書式確認
        sut = Edge(0, 1, Decimal('2'))
        self.assertEqual('[0 - 1, cost: 2]', str(sut))

    def test_repr(self):
        # __reprの書式確認
        sut = Edge(0, 1, Decimal('2'))
        self.assertEqual("Edge(0, 1, Decimal('2'))", repr(sut))

    def test_change_var(self):
        # インスタンス変数が変更できないことを確認
        sut = Edge(0, 1, Decimal(2))
        with self.assertRaises(AttributeError):
            sut.node1 = 1
        with self.assertRaises(AttributeError):
            sut.node2 = 2
        with self.assertRaises(AttributeError):
            sut.cost = Decimal(3)
