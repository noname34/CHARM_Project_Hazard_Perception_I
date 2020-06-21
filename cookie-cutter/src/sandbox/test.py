#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception


import os

import numpy as np
import pandas as pd

from configuration import PATH_DIR_INTERIM_DATA, ANTICIPATION_TIME, THRESHOLD_DISTANCE, PATH_DIR_REPORT_FIGURE, \
    IGNORE_3D
from data.external.dataset_data_format import CENTER_X_COORD, CENTER_Z_COORD, CENTER_Y_COORD, SCENARIO_DIR_PATTERN, \
    LABEL_FILES_PATTERN, TRACKER_ID, VELOCITY_FILES_PATTERN, MEAN_SPEED, FRAME_DURATION, FRAME_NUMBER_OF_DIGITS, \
    APPROX_FRAME_DURATION, LABEL
from src.libraries.myFileSystemLib import getNextFile, getFirstFileInDir, log_alert
from src.libraries.myMathLib import closestDistanceBetweenLines, get_next_position
from src.visualization.visualize import plot3DLines

def main():
    """
    Compute vehicles future trajectories
    v0: calculate instrumented car's velocity vector based on its speed and the frame duration
    v1: calculate instrumented car's velocity vector based on velocity vector information from GPS module
    :return:
    """
    # current scenario
    scenario = "scenario_002"
    trajectories_coordinates = []  # used to store all trajectories

    # INSTRUMENTED CAR
    # current frame
    path_at_i = getFirstFileInDir(PATH_DIR_INTERIM_DATA + scenario, VELOCITY_FILES_PATTERN)
    # path_at_i = PATH_DIR_INTERIM_DATA + scenario + "/CAN_vel_146.csv"

    # frame_i id
    frame_name = os.path.basename(path_at_i).split(".")[0]  # frame name without ext
    frame_i_id = frame_name[len(frame_name) - FRAME_NUMBER_OF_DIGITS:]  # frame number

    # instrumented car's speed and frame duration
    ref_car_at_i = pd.read_csv(path_at_i)
    speed_at_i = ref_car_at_i.loc[0, MEAN_SPEED]
    # distance the instrumented car drives between b0 and b1
    distance = speed_at_i * ANTICIPATION_TIME  # distance = speed * time
    b0 = np.array([0, 0, 0])  # reference point
    b1 = np.array([b0[0] + distance, b0[1], b0[2]])  # position at frame_ii
    orientation_vector = np.subtract(b1, b0)
    print("orientation_vector instrumented car: ", orientation_vector)
    print("prototype v0", distance)
    bn = get_next_position(b0, orientation_vector, ANTICIPATION_TIME)
    if IGNORE_3D:
        bn[2] = 0
    trajectories_coordinates.insert(len(trajectories_coordinates), b0)
    trajectories_coordinates.insert(len(trajectories_coordinates), bn)

    # SURROUNDING OBJECTS
    # get scenario and frame i
    path_frame_at_i = getFirstFileInDir(PATH_DIR_INTERIM_DATA + scenario, LABEL_FILES_PATTERN)
    # path_frame_at_i = PATH_DIR_PROCESSED_DATA + scenario + "/labels_3d1_146.csv"

    # get position at frame_i
    objects_at_i = pd.read_csv(path_frame_at_i,
                               usecols=[TRACKER_ID, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD])
    number_of_objects = len(objects_at_i.index)  # number of objects in the frame
    for object_index in range(0, number_of_objects):
        id_object_j = objects_at_i.loc[object_index, TRACKER_ID]
        a0 = np.array(
            [objects_at_i.loc[object_index, CENTER_X_COORD], objects_at_i.loc[object_index, CENTER_Y_COORD],
             objects_at_i.loc[object_index, CENTER_Z_COORD]])
        if a0[0] < 0:  # the considered traffic participant is behind the instrumented car --> do not consider this
            # object
            continue
        if IGNORE_3D:
            a0[2] = 0
        # get object's position at frame_i+1 (frame_ii)
        path_frame_at_ii = getNextFile(path_frame_at_i, LABEL_FILES_PATTERN, SCENARIO_DIR_PATTERN)
        objects_at_ii = pd.read_csv(path_frame_at_ii,
                                    usecols=[TRACKER_ID, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD])
        # look for id_object_0's position at frame i+1
        obj = objects_at_ii[objects_at_ii[TRACKER_ID] == id_object_j]
        a1 = np.array([obj.loc[object_index, CENTER_X_COORD], obj.loc[object_index, CENTER_Y_COORD],
                       obj.loc[object_index, CENTER_Z_COORD]])
        if IGNORE_3D:
            a1[2] = 0

        a1[0] -= distance  # subtract the distance travelled by the ego car from the vehicle's position
        # compute orientation vector
        orientation_vector = np.subtract(a1, a0)
        # compute id_object_0's position after anticipation time
        an = get_next_position(a0, orientation_vector, ANTICIPATION_TIME)
        trajectories_coordinates.insert(len(trajectories_coordinates), a0)
        trajectories_coordinates.insert(len(trajectories_coordinates), an)

        # compute shortest distance
        shortest_distance = closestDistanceBetweenLines(a0, an, b0, bn, clampAll=True)
        print("shortest_distance: ", shortest_distance)
        if shortest_distance <= THRESHOLD_DISTANCE:
            print("danger in scenario :  frame: , with object having ID: ", scenario, frame_i_id, id_object_j)
            log_alert('distance_checker', scenario, frame_i_id, objects_at_i.loc[object_index, LABEL],
                      id_object_j, THRESHOLD_DISTANCE, shortest_distance)

    # plot trajectories and shortest distance
    context = "prototypeV1.0/"
    path = PATH_DIR_REPORT_FIGURE + context + scenario
    if not (os.path.exists(os.path.dirname(path))):
        os.mkdir(os.path.dirname(path))
    plot3DLines(trajectories_coordinates, save_plot=False, scenario_name=scenario, frame_name=frame_i_id,
                path=path)


if __name__ == '__main__':
    main()
