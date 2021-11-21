#!/usr/bin/env python3

import unittest
from collections import OrderedDict

import pigment


class PigmentTest(unittest.TestCase):

    def test_simple(cls) -> None:
        partitions = pigment.get_best_partition(OrderedDict((
            (1, (2, 3)),
            (2, (3, 4)),
        )))
        cls.assertEqual(partitions, [[1, 4], [2], [3]])


    def test_boilerplate(cls) -> None:
        BUFFET = "BUFFET"
        AHA = "AHA"
        BHA = "BHA"
        HIPPIE = "HIPPIES"
        ELAA = "ELAA"
        RETINOL = "RETINOL"
        partitions = pigment.get_best_partition(OrderedDict([
            [BUFFET, [AHA, BHA, HIPPIE, ELAA, RETINOL]],
            [AHA, [RETINOL]],
            [BHA, [RETINOL]],
            [HIPPIE, [AHA, BHA, RETINOL]],
            [ELAA, [AHA, BHA, RETINOL]],
        ]))
        cls.assertEqual(partitions, [
            ["BUFFET"], ["AHA", "BHA"], ["HIPPIES", "ELAA"], ["RETINOL"]
        ])

    def test_complete(cls) -> None:
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        E = "E"
        partitions = pigment.get_best_partition(OrderedDict([
            [A, [B, C, D, E]],
            [B, [C, D, E]],
            [C, [D, E]],
            [D, [E]],
        ]))
        cls.assertEqual(partitions, [[A], [B], [C], [D], [E]])

    def test_freedom(cls):
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        E = "E"
        partitions = pigment.get_best_partition(OrderedDict([
            [A, []],
            [B, []],
            [C, []],
            [D, []],
            [E, []],
        ]))
        cls.assertEqual(partitions, [[A, B, C, D, E]])


if __name__ == "__main__":
    unittest.main()
