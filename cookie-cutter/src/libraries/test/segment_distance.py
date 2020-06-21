#!/user/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from src.libraries.myMathLib import point_to_segment_distance, euclidean_distance_3d, lineseg_dist, distance_numpy


def main():
    expected = 5
    a0 = np.array([3, 1, -1])
    a1 = np.array([5, 2, 1])
    c = np.array([0, 2, 3])
    print(lineseg_dist(c, a0, a1), point_to_segment_distance(c, a0, a1), distance_numpy(c, a0, a1), expected)

    expected = 1
    a0 = np.array([3, 2, 1])
    a1 = np.array([4, 2, 1])
    c = np.array([0, 2, 0])
    print(lineseg_dist(c, a0, a1), point_to_segment_distance(c, a0, a1), distance_numpy(c, a0, a1), expected)


if __name__ == '__main__':
    main()
