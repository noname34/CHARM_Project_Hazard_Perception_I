#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 01.05.20
# Context: CHARM PROJECT - Harzard perception
import numpy as np
from src.libraries.myMathLib import closestDistanceBetweenLines
import matplotlib.pyplot as plt


def main():
    ax = plt.axes(projection='3d')
    a1 = np.array([13.43, 21.77, 46.81])
    a0 = np.array([27.83, 31.74, -26.60])
    b0 = np.array([77.54, 7.53, 6.22])
    b1 = np.array([26.99, 12.39, 11.18])
    print("closestDistanceBetweenLines: ", closestDistanceBetweenLines(a0, a1, b0, b1, clampAll=True))
    # ax.plot([20.29994362, 26.99], [26.5264818, 12.39], zs=[11.78759994, 11.18], color='red')
    ax.plot([a1[0], a0[0]], [a1[1], a0[1]], zs=[a1[2], a0[2]], color='blue')
    ax.plot([b1[0], b0[0]], [b1[1], b0[1]], zs=[b1[2], b0[2]], color='green')
    plt.show()

    ax = plt.axes(projection='3d')
    a0 = np.array([-1.0264718499965966, 9.6163341007195407e-007, 0.0])
    a1 = np.array([0.91950808032415809, -1.0094441192690283e-006, 0.0])
    b0 = np.array([-1.0629447383806110, 9.2709540082141753e-007, 0.0])
    b1 = np.array([1.0811583868227901, -1.0670017179567367e-006, 0.0])
    ax.plot([a1[0], a0[0]], [a1[1], a0[1]], zs=[a1[2], a0[2]], color='blue')
    ax.plot([b1[0], b0[0]], [b1[1], b0[1]], zs=[b1[2], b0[2]], color='green')
    print("closestDistanceBetweenLines: ", closestDistanceBetweenLines(a0, a1, b0, b1, clampAll=True))
    plt.show()


    ax = plt.axes(projection='3d')
    a0 = np.array([0.77998990099877119, 0.61192502360790968, -0.22703111823648214])
    a1 = np.array([0.53215344529598951, 0.85724585503339767, -0.10102437809109688])
    b0 = np.array([-0.21277333982288837, 0.35091548087075353, -0.49557160679250956])
    b1 = np.array([0.11881479667499661, 0.022494725417345762, -0.66426620958372951])
    ax.plot([a1[0], a0[0]], [a1[1], a0[1]], zs=[a1[2], a0[2]], color='blue')
    ax.plot([b1[0], b0[0]], [b1[1], b0[1]], zs=[b1[2], b0[2]], color='green')
    plt.show()
    print("closestDistanceBetweenLines: ", closestDistanceBetweenLines(a0, a1, b0, b1, clampAll=True))


main()
