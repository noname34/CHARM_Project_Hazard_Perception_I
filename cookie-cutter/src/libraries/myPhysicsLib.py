#!/user/bin/env python3#
# -*- coding: utf-8 -*-
from data.external.environmental_conditions import COEF_FRICTION_ASPHALT


def reaction_distance(speed, reaction_time):
    return round(((speed * reaction_time) / 3.60), 3)


def braking_distance(speed, friction_coef):
    return round((pow(speed, 2) / (250.0 * friction_coef)), 3)


def stopping_distance(speed, reaction_time, friction_coef):
    return reaction_distance(speed, reaction_time) + braking_distance(speed, friction_coef)
