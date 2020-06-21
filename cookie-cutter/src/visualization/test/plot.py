#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception


import matplotlib.pyplot as plt
import numpy as np

from src.visualization.visualize import plot3DLines


def main():
    """
    Test script for plot visualisations
    :return:
    """

    '''
    a1 = np.array([2, 0, 50])
    a0 = np.array([2, 100, 50])
    b0 = np.array([10, 0, 50])
    b1 = np.array([10, 100, 50])
    d1 = np.array([20.29994362, 26.5264818, 11.78759994])
    d0 = np.array([26.99, 12.39, 11.18])
    '''
    a1 = np.array([13.43, 21.77, 46.81])
    a0 = np.array([27.83, 31.74, -26.60])
    b0 = np.array([77.54, 7.53, 6.22])
    b1 = np.array([26.99, 12.39, 11.18])
    d1 = np.array([20.29994362, 26.5264818, 11.78759994])
    d0 = np.array([26.99, 12.39, 11.18])

    list_lines = [a1, a0, b0, b1, d1, d0]
    plot3DLines(list_lines)  # multiple_subplots=True)


if __name__ == '__main__':
    main()
