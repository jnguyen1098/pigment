#!/usr/bin/env python3

import pigment
import unittest
from collections import OrderedDict

class PigmentTest(unittest.TestCase):

    def test_simple(cls):
        partitions = pigment.get_partitions(OrderedDict((
            (1, (2, 3)),
            (2, (3, 4)),
        )))
        cls.assertEqual(partitions, [[1, 4], [2], [3]])


    def test_boilerplate(cls):
        BUFFET = "BUFFET"
        AHA = "AHA"
        BHA = "BHA"
        HIPPIE = "HIPPIES"
        ELAA = "ELAA"
        RETINOL = "RETINOL"
        partitions = pigment.get_partitions(OrderedDict((
            (BUFFET, [AHA, BHA, HIPPIE, ELAA, RETINOL]),
            (AHA, [RETINOL]),
            (BHA, [RETINOL]),
            (HIPPIE, [AHA, BHA, RETINOL]),
            (ELAA, [AHA, BHA, RETINOL]),
        )))
        cls.assertEqual(partitions, [
            ["BUFFET"], ["AHA", "BHA"], ["HIPPIES", "ELAA"], ["RETINOL"]
        ])


if __name__ == "__main__":
    unittest.main()
