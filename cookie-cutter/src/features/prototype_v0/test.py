#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os

import pandas as pd
import numpy as np

from configuration import PATH_DIR_INTERIM_DATA, PATH_DIR_REPORT_FIGURE
from data.external.dataset_data_format import LABEL, RADIUS, TRACKER_ID, CENTER_X_COORD, FRAME_NUMBER_OF_DIGITS, \
    REFERENCE_POINT_3D, CENTER_Y_COORD, CENTER_Z_COORD
from data.external.environmental_conditions import COEF_FRICTION_ASPHALT
from src.libraries.myFileSystemLib import log_alert
from src.libraries.myPhysicsLib import stopping_distance
from src.visualization.visualize import plot3DLines, plot3DPoints


def main():
    trajectories_coordinates = []
    reaction_time = 1.5
    print("reaction_time: ", reaction_time)

    scenario = "scenario_002"
    filename = "CAN_vel_000.csv"
    path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
    frame_name = os.path.basename(path).split(".")[0]  # frame name without ext
    frame_id = frame_name[len(frame_name) - FRAME_NUMBER_OF_DIGITS:]  # frame number
    # print(path)
    df = pd.read_csv(path)
    # print(df)
    speed = df.loc[0, "mean_speed"]
    minimal_distance = stopping_distance(speed, reaction_time, COEF_FRICTION_ASPHALT)
    print("minimal_distance distance: ", minimal_distance)

    df_scene = pd.read_csv(PATH_DIR_INTERIM_DATA + scenario + '/' + "labels_3d1_000.csv")

    subset_scene = df_scene[[LABEL, TRACKER_ID, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD, RADIUS]]

    origin = REFERENCE_POINT_3D
    trajectories_coordinates.insert(len(trajectories_coordinates), origin)

    # print(subset_scene)
    for i in range(len(subset_scene.index)):
        x_pos_to_object_i = subset_scene.loc[i, CENTER_X_COORD]
        object_position = np.array([subset_scene.loc[i, CENTER_X_COORD], subset_scene.loc[i, CENTER_Y_COORD],
                                    subset_scene.loc[i, CENTER_Z_COORD]])
        object_position[2] = 0  # TODO ASSUMPTION PROTOTYPE 1!!!
        if x_pos_to_object_i < 0:  # consider only vehicles that are in front of the instrumented car
            continue
        trajectories_coordinates.insert(len(trajectories_coordinates), object_position)
        distance_to_object_i = subset_scene.loc[i, RADIUS]
        # print("distance :      object id : ", subset_scene.loc[i, LABEL], subset_scene.loc[i, TRACKER_ID],
        # distance_to_object_i)
        if distance_to_object_i < minimal_distance:
            print("WARNING DISTANCE TO OBJECT ", subset_scene.loc[i, LABEL], subset_scene.loc[i, TRACKER_ID],
                  "IS NOT APPROPRIATE: ",
                  distance_to_object_i)
            log_alert('distance_checker v0', scenario, frame_id, subset_scene.loc[i, LABEL], subset_scene.loc[i, TRACKER_ID], minimal_distance,
                      distance_to_object_i)

    print(trajectories_coordinates)
    context = "prototypeV0/"
    path = PATH_DIR_REPORT_FIGURE + context + scenario
    if not (os.path.exists(os.path.dirname(path))):
        os.mkdir(os.path.dirname(path))
    plot3DPoints(trajectories_coordinates, save_plot=False, scenario_name=scenario, frame_name=frame_id, path=path)


if __name__ == '__main__':
    main()
