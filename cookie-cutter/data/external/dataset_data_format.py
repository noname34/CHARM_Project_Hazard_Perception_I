#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception


# Dataset format: https://usa.honda-ri.com/H3D


import numpy as np


FRAME_NUMBER_OF_DIGITS = 3  # all files are named CAN_vel_xxx.csv, labels_3d1_xxx.txt --> frame ID has 3 digits
APPROX_FRAME_DURATION = 0.09  # seconds. see frame_duration() function for more information about mean frame duration
REFERENCE_POINT_3D = np.array([0, 0, 0])


# files name pattern in dir /data/interim
VELOCITY_FILES_PATTERN = "CAN_vel_*.csv"
LABEL_FILES_PATTERN = "labels_3d1_*.csv"
GPS_FILES_PATTERN = "gps_*.csv"
SCENARIO_DIR_PATTERN = "scenario_*"


# Column names in files labels_xxx.txt in /data/raw
LABEL = 'label'
TRACKER_ID = 'trackerID'
STATE = 'state'
CENTER_X_COORD = 'c_x'
CENTER_Y_COORD = 'c_y'
CENTER_Z_COORD = 'c_z'
LENGTH_X_COORD = 'l_x'
LENGTH_Y_COORD = 'l_y'
LENGTH_Z_COORD = 'l_z'
YAW = 'yaw'
RADIUS = 'radius'
POLAR_ANGLE = 'polar angle'
AZIMUTH_ANGLE = 'azimuth angle'

# Column names in files CAN_vel_*.csv
SPEED = 'speed'  # raw data
TIMESTAMP = 'timestamps'  # raw data
MEAN_SPEED = 'mean_speed'  # interim data
FRAME_DURATION = 'frame_duration'  # interim data

# Column names in files gps_*.csv
VELOCITY_X = "Vel_x"
VELOCITY_Y = "Vel_y"
VELOCITY_Z = "Vel_z"
