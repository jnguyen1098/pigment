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
        a_test = "A"
        b_test = "B"
        c_test = "C"
        d_test = "D"
        e_test = "E"
        partitions = pigment.get_best_partition(
            OrderedDict(
                (
                    (a_test, [b_test, c_test, d_test, e_test]),
                    (b_test, [c_test, d_test, e_test]),
                    (c_test, [d_test, e_test]),
                    (d_test, [e_test]),
                )
            )
        )
        self.assertEqual(partitions, [[a_test], [b_test], [c_test], [d_test], [e_test]])

    def test_freedom(self) -> None:
        """Test an instance where all ingredients are compatible."""
        a_test = "A"
        b_test = "B"
        c_test = "C"
        d_test = "D"
        e_test = "E"
        partitions = pigment.get_best_partition(
            OrderedDict(
                (
                    (a_test, []),
                    (b_test, []),
                    (c_test, []),
                    (d_test, []),
                    (e_test, []),
                )
            )
        )
        self.assertEqual(partitions, [[a_test, b_test, c_test, d_test, e_test]])


if __name__ == "__main__":
    unittest.main()
