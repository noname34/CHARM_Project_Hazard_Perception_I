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
    IGNORE_3D, PRECISION_FLOAT
from data.external.dataset_data_format import CENTER_X_COORD, CENTER_Z_COORD, CENTER_Y_COORD, SCENARIO_DIR_PATTERN, \
    LABEL_FILES_PATTERN, TRACKER_ID, VELOCITY_FILES_PATTERN, MEAN_SPEED, FRAME_DURATION, FRAME_NUMBER_OF_DIGITS, \
    GPS_FILES_PATTERN, VELOCITY_X, VELOCITY_Y, VELOCITY_Z, REFERENCE_POINT_3D, APPROX_FRAME_DURATION, LABEL
from src.libraries.myFileSystemLib import getNextFile, getFirstFileInDir, log_alert
from src.libraries.myMathLib import closestDistanceBetweenLines, get_next_position, euclidean_distance_3d, \
    get_previous_position
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
    frame = "138"
    trajectories_coordinates = []  # used to store all trajectories

    ## INSTRUMENTED CAR
    # current frame
    path_at_i = PATH_DIR_INTERIM_DATA + scenario + "/gps_" + frame + ".csv"
    # frame_i id
    frame_name = os.path.basename(path_at_i).split(".")[0]  # frame name without ext
    frame_i_id = frame_name[len(frame_name) - FRAME_NUMBER_OF_DIGITS:]  # frame number
    # instrumented velocity direction vector
    ref_car_at_i = pd.read_csv(path_at_i, float_precision="round_trip")
    # distance the instrumented car drives between b0 and bn
    b0 = REFERENCE_POINT_3D  # reference point
    orientation_vector = np.array([ref_car_at_i.loc[0, VELOCITY_X], ref_car_at_i.loc[0, VELOCITY_Y],
                                   ref_car_at_i.loc[0, VELOCITY_Z]])
    if IGNORE_3D:
        orientation_vector[2] = 0
    bn = get_next_position(b0, orientation_vector, ANTICIPATION_TIME)
    if IGNORE_3D:
        bn[2] = 0
    distance_travelled_instr_car = euclidean_distance_3d(b0, bn)
    v = bn - b0  # vector from point b0 to b0+ANTICIPATION_TIME (b0 to bn) for the instrumented car

    trajectories_coordinates.insert(len(trajectories_coordinates), b0)
    trajectories_coordinates.insert(len(trajectories_coordinates), bn)


    # SURROUNDING OBJECTS
    # get scenario and frame i
    path_frame_at_i = PATH_DIR_INTERIM_DATA + scenario + "/labels_3d1_" + frame + ".csv"
    # get position at frame_i
    objects_at_i = pd.read_csv(path_frame_at_i, usecols=[TRACKER_ID, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD])
    number_of_objects = len(objects_at_i.index)
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
        # get object's position at frame_i+ANTICIPATION_TIME (frame_ii)
        n_frames_forward = ANTICIPATION_TIME / APPROX_FRAME_DURATION  # number of frames to anticipate
        path_frame_at_ii = getNextFile(path_frame_at_i, LABEL_FILES_PATTERN, SCENARIO_DIR_PATTERN,
                                       increment=n_frames_forward)
        objects_at_ii = pd.read_csv(path_frame_at_ii, usecols=[LABEL, TRACKER_ID, CENTER_X_COORD, CENTER_Y_COORD,
                                                               CENTER_Z_COORD])
        # look for id_object_j's position at frame i+ANTICIPATION_TIME
        obj = objects_at_ii[objects_at_ii[TRACKER_ID] == id_object_j]
        if len(obj.index) == 0:  # obj does not exist anymore in the traffic scene after ANTICIPATION_TIME
            continue
        an = np.array([obj[CENTER_X_COORD].iloc[0], obj[CENTER_Y_COORD].iloc[0], obj[CENTER_Z_COORD].iloc[0]])
        if IGNORE_3D:
            an[2] = 0
        # referentiel adjustement
        an_adjusted = np.add(an, v)
        # vector the instrumented car travelled during ANTICPATION_TIME

        trajectories_coordinates.insert(len(trajectories_coordinates), a0)
        trajectories_coordinates.insert(len(trajectories_coordinates), an_adjusted)

        # compute shortest distance
        shortest_distance = round(closestDistanceBetweenLines(a0, an, b0, bn, clampAll=True), PRECISION_FLOAT)
        if shortest_distance <= THRESHOLD_DISTANCE:
            # log alert when vehicles are too close to the instrumented car
            log_alert('distance_checker v0', scenario, frame_i_id, objects_at_i.loc[object_index, LABEL],
                      id_object_j, THRESHOLD_DISTANCE, shortest_distance)

    # plot trajectories and shortest distance
    context = "prototypeV1.1/"
    path = PATH_DIR_REPORT_FIGURE + context + scenario
    if not (os.path.exists(os.path.dirname(path))):
        os.mkdir(os.path.dirname(path))
    plot3DLines(trajectories_coordinates, save_plot=False, scenario_name=scenario, frame_name=frame_i_id,
                path=path)


if __name__ == '__main__':
    main()