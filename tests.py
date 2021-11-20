#!/usr/bin/env python3

import pigment
import unittest
from collections import OrderedDict

class PigmentTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print("setup fixture")

    def test_simple(cls):
        partitions = pigment.get_partitions(OrderedDict((
            (1, (2, 3)),
            (2, (3, 4)),
        )))
        cls.assertEqual(partitions, [[1, 4], [2], [3]])


if __name__ == "__main__":
    unittest.main()
