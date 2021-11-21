#!/usr/bin/env python3
"""Unit tests for Pigment."""

import unittest
from collections import OrderedDict

import pigment


class PigmentTest(unittest.TestCase):
    """Test class for Pigment."""

    def test_simple(self) -> None:
        """Run simple test consisting of just integers."""
        partitions = pigment.get_best_partition(
            OrderedDict(
                (
                    (1, (2, 3)),
                    (2, (3, 4)),
                )
            )
        )
        self.assertEqual(partitions, [[1, 4], [2], [3]])

    def test_boilerplate(self) -> None:
        """Run the boilerplate example test."""
        buffet = "BUFFET"
        aha = "AHA"
        bha = "BHA"
        hippie = "HIPPIE"
        elaa = "ELAA"
        retinol = "RETINOL"
        partitions = pigment.get_best_partition(
            OrderedDict(
                (
                    (buffet, [aha, bha, hippie, elaa, retinol]),
                    (aha, [retinol]),
                    (bha, [retinol]),
                    (hippie, [aha, bha, retinol]),
                    (elaa, [aha, bha, retinol]),
                )
            )
        )
        self.assertEqual(partitions, [[buffet], [aha, bha], [hippie, elaa], [retinol]])

    def test_complete(self) -> None:
        """Test an instance where all ingredients are incompatible."""
        a = "A"
        b = "B"
        c = "C"
        d = "D"
        e = "E"
        partitions = pigment.get_best_partition(
            OrderedDict(
                (
                    (a, [b, c, d, e]),
                    (b, [c, d, e]),
                    (c, [d, e]),
                    (d, [e]),
                )
            )
        )
        self.assertEqual(partitions, [[a], [b], [c], [d], [e]])

    def test_freedom(self) -> None:
        """Test an instance where all ingredients are compatible."""
        a = "A"
        b = "B"
        c = "C"
        d = "D"
        e = "E"
        partitions = pigment.get_best_partition(
            OrderedDict(
                (
                    (a, []),
                    (b, []),
                    (c, []),
                    (d, []),
                    (e, []),
                )
            )
        )
        self.assertEqual(partitions, [[a, b, c, d, e]])


if __name__ == "__main__":
    unittest.main()
