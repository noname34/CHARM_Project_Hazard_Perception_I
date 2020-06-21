#!/user/bin/env python3
# -*- coding: utf-8 -*-

# Created by Kevin Bürgisser at 01.05.20
# CHARM PROJECT - Harzard perception

import unittest
import numpy as np

from src.libraries.myMathLib import closestDistanceBetweenLines


class MyTestCase(unittest.TestCase):
    def test_distance_seg_to_seg(self):
        PRECISION=15
        # src: geometrictools.com/Documentation/DistanceLine3Line3.pdf,
        # Example 3. An example where forcing the parallel case to start the search at s = 0 fails
        expected_result = 0.9829239711648873
        a0 = np.array([0.77998990099877119, 0.61192502360790968, -0.22703111823648214])
        a1 = np.array([0.53215344529598951, 0.85724585503339767, -0.10102437809109688])
        b0 = np.array([-0.21277333982288837, 0.35091548087075353, -0.49557160679250956])
        b1 = np.array([0.11881479667499661, 0.022494725417345762, -0.66426620958372951])
        distance = closestDistanceBetweenLines(a0, a1, b0, b1, clampAll=True)
        self.assertEqual(round(distance, PRECISION), round(expected_result, PRECISION))


if __name__ == '__main__':
    unittest.main()
