#!/usr/bin/env python3

import pigment
import unittest

class PigmentTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print("setup fixture")

    def test_lmao(cls):
        BUFFET = "Buffet + Copper Peptides"
        AHA = "Alpha Hydroxy Acids"
        BHA = "Beta Hydroxy Acids"
        HIPPIE = "Mad Hippie"
        ELAA = "Ethylated Ascorbic Acid"
        RETINOL = "Retinol"
        
        CONFLICTS = {
            BUFFET: [AHA, BHA, HIPPIE, ELAA, RETINOL],
            AHA: [RETINOL],
            BHA: [RETINOL],
            HIPPIE: [AHA, BHA, RETINOL],
            ELAA: [AHA, BHA, RETINOL],
        }
        result = pigment.get_partitions(CONFLICTS)
        print(result)
        cls.assertTrue(1)


if __name__ == "__main__":
    unittest.main()
