#!/user/bin/env python3
# -*- coding: utf-8 -*-

import math
from math import radians
import numpy as np
from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm


# implementation of the pythagorean theorem. The value that is missing is set to 0 when arriving at the function
from configuration import PRECISION_FLOAT, IGNORE_3D


def pythagorean_theorem(a, b, c):
    if c == 0:
        return math.sqrt(a * a + b * b)
    elif b == 0:
        return math.sqrt(c * c - a * a)
    elif a == 0:
        return math.sqrt(c * c - b * b)


# gives the distance between two points in the space
def euclidean_distance_3d(p, o):
    return round(np.linalg.norm(p - o), PRECISION_FLOAT)


def cart2sph(p):
    x = p[0]
    y = p[1]
    z = p[2]
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    if IGNORE_3D:
        pol = radians(90)
    else:
        pol = np.arctan2(z, hxy)

    az = np.arctan2(y, x)
    spherical_coord = np.array([r, pol, az])
    return spherical_coord


# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def point_to_segment_distance(P, A, B):
    """ segment line AB, point P, where each one is an array([x, y]) """
    if all(A == P) or all(B == P):
        return 0
    if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > pi / 2:
        return norm(P - A)
    if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > pi / 2:
        return norm(P - B)
    return norm(cross(A-B, A-P))/norm(B-A)


# src : https://stackoverflow.com/questions/2824478/shortest-distance-between-two-line-segments
def closestDistanceBetweenLines(a0, a1, b0, b1, clampAll=False, clampA0=False, clampA1=False, clampB0=False,
                                clampB1=False):
    ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return the closest points on each segment and their distance. For closest distance between lines (not
        segments), set clampAll to False. For segments, set clampAll to True
    '''

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0 = True
        clampA1 = True
        clampB0 = True
        clampB1 = True

    # Calculate denominator
    A =np.subtract(a1, a0)
    B =np.subtract(b1, b0)
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    # both objects are static
    if magA == 0.0 and magB == 0.0:
        return euclidean_distance_3d(A, B)#, A, B
    # object A is static, not B. Calculate distance between A and segment from b0 to b1
    if magA == 0.0:
        return point_to_segment_distance(A, b0, b1)
    # object B is static, not A. Calculate distance between B and segment from a0 to a1
    if magB == 0.0:
        return point_to_segment_distance(B, a0, a1)

    _A = A / magA
    _B = B / magB

    cross = np.cross(_A, _B)
    denom = np.linalg.norm(cross) ** 2

    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A, (b0 - a0))

        # Overlap only possible with clamping
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A, (b1 - a0))

            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.absolute(d0) < np.absolute(d1):
                        return np.linalg.norm(a0 - b0)#,a0, b0
                    return np.linalg.norm(a0 - b1)#,a0, b1

            # Is segment B after A?
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.absolute(d0) < np.absolute(d1):
                        return np.linalg.norm(a1 - b0)#,a1, b0
                    return np.linalg.norm(a1 - b1)#,a1, b1

        # Segments overlap, return distance between parallel segments
        return np.linalg.norm(((d0 * _A) + a0) - b0)#,None, None

    # Lines criss-cross: Calculate the projected closest points
    t = (b0 - a0)
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA / denom
    t1 = detB / denom

    pA = a0 + (_A * t0)  # Projected closest point on segment A
    pB = b0 + (_B * t1)  # Projected closest point on segment B

    # Clamp projections
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1

        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1

        # Clamp projection A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B, (pA - b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)

        # Clamp projection B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A, (pB - a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)

    return np.linalg.norm(pA - pB)#, pA, pB


def get_next_position(start_position, orientation_vector, t):
    return np.add(start_position, orientation_vector * t)


def get_previous_position(stop_position, orientation_vector, t):
    return np.subtract(stop_position, orientation_vector * t)
