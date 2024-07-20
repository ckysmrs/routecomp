import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from binary_heap import BinaryHeap

class BinaryHeapTest(unittest.TestCase):
    def test_get_min(self):
        # 最小値のサテライトを返す
        satelittes = (4, 2, 6, 3, 0)
        keys = (Decimal('0.7'), Decimal('0.2'), Decimal('0.4'), Decimal('0.8'), Decimal('0.3'))
        sut = BinaryHeap()
        for k, s in zip(keys, satelittes):
            sut.insert(k, s)
        self.assertEqual(sut.delete_min(), 2)
        self.assertEqual(sut.delete_min(), 0)
        self.assertEqual(sut.delete_min(), 6)
        self.assertEqual(sut.delete_min(), 4)
        self.assertEqual(sut.delete_min(), 3)

    def test_same_satelette(self):
        # 同じサテライトに登録すると例外を出す
        sut = BinaryHeap()
        sut.insert(Decimal('1'), 0)
        with self.assertRaises(ValueError, msg='Error: satellite already in heap'):
            sut.insert(Decimal('2'), 0)

    def test_len(self):
        # サイズを返す
        sut = BinaryHeap()
        self.assertEqual(len(sut), 0)
        sut.insert(Decimal('1'), 0)
        self.assertEqual(len(sut), 1)
        sut.delete_min()
        self.assertEqual(len(sut), 0)

    def test_no_data(self):
        # データが無いのに取り出そうとすると例外を出す
        sut = BinaryHeap()
        with self.assertRaises(IndexError, msg='Error: empty heap'):
            sut.delete_min()

    def test_change_key(self):
        # キーを変える
        sut = BinaryHeap()
        sut.insert(Decimal('0.1'), 0)
        sut.insert(Decimal('0.2'), 1)
        sut.change_key(Decimal('0.3'), 0)
        self.assertEqual(sut.delete_min(), 1)

    def test_remove(self):
        # サテライト指定でキーを削除
        satelittes = (4, 2, 6, 3, 0)
        keys = (Decimal('0.7'), Decimal('0.2'), Decimal('0.4'), Decimal('0.8'), Decimal('0.3'))
        sut = BinaryHeap()
        for k, s in zip(keys, satelittes):
            sut.insert(k, s)
        sut.remove(6)
        self.assertEqual(sut.delete_min(), 2)
        self.assertEqual(sut.delete_min(), 0)
        self.assertEqual(sut.delete_min(), 4)
        self.assertEqual(sut.delete_min(), 3)

    def test_clear(self):
        # データのクリア
        satelittes = (4, 2, 6, 3, 0)
        keys = (Decimal('0.7'), Decimal('0.2'), Decimal('0.4'), Decimal('0.8'), Decimal('0.3'))
        sut = BinaryHeap()
        for k, s in zip(keys, satelittes):
            sut.insert(k, s)
        self.assertEqual(len(sut), 5)
        sut.clear()
        self.assertEqual(len(sut), 0)
        for k, s in zip(keys, satelittes):
            sut.insert(k, s)
        self.assertEqual(len(sut), 5)
        self.assertEqual(sut.delete_min(), 2)
        self.assertEqual(sut.delete_min(), 0)
        self.assertEqual(sut.delete_min(), 6)
        self.assertEqual(sut.delete_min(), 4)
        self.assertEqual(sut.delete_min(), 3)

    def test_contains_satellite(self):
        # サテライトの存在の確認
        sut = BinaryHeap()
        sut.insert(Decimal('0.1'), 1)
        self.assertTrue(sut.contains_satellite(1))
        self.assertFalse(sut.contains_satellite(2))
