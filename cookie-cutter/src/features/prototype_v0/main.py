#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 03.04.2020
# Context: CHARM PROJECT - Harzard perception

import fnmatch
import os
import pandas as pd
from configuration import PATH_DIR_INTERIM_DATA, PATH_DIR_REPORT_FIGURE, IGNORE_3D, PRECISION_FLOAT
from data.external.dataset_data_format import *
from data.external.environmental_conditions import COEF_FRICTION_ASPHALT
from src.libraries.myFileSystemLib import log_alert
from src.libraries.myPhysicsLib import stopping_distance
from src.visualization.visualize import plot3DPoints


def main(plot=False):
    """
    This method aims to check whether distances between the instrumented car and other participants is appropriate.
    The method computes the stopping distance of the instrumented car based on the reaction time of the driver,
    friction coefficient of the surface the car drives on and the speed of the car.
    In the case, the computed distance is not appropriate, the method logs the alert into /reports/alerts/distance_checker.csv file

    :return: nothing
    """

    point_coordinates = []  # used to store all point around the instrumented car
    reaction_time = 1.5

    # get all scenarios of the dataset
    scenarios = os.listdir(PATH_DIR_INTERIM_DATA)
    scenarios.sort()  # it's important to sort them because by default they are listed randomly
    for scenario in scenarios:
        path_scenario = PATH_DIR_INTERIM_DATA + scenario  # build path
        print(path_scenario)
        if fnmatch.fnmatch(scenario, SCENARIO_DIR_PATTERN):  # check found dir is a scenario
            if not (os.path.exists(path_scenario)):  # create dir if it does not exist yet
                os.mkdir(path_scenario)
            filenames = os.listdir(path_scenario)  # list files in scenario directory
            filenames.sort()
            for filename in filenames:
                if fnmatch.fnmatch(filename,
                                   VELOCITY_FILES_PATTERN):  # look for velocity files (we need speed information!)
                    frame_name = filename.split(".")[0]  # frame name without ext
                    frame_id = frame_name[len(frame_name) - FRAME_NUMBER_OF_DIGITS:]  # frame number
                    df = pd.read_csv(path_scenario + "/" + filename)
                    speed = df.loc[0, MEAN_SPEED]  # speed information
                    # compute stopping distance
                    minimal_distance = round(stopping_distance(speed, reaction_time,
                                                               COEF_FRICTION_ASPHALT), PRECISION_FLOAT)
                    path_label = path_scenario + '/' + "labels_3d1_" + frame_id + ".csv"
                    if not os.path.exists(path_label):
                        continue
                    df_scene = pd.read_csv(path_label)
                    # get other vehicles positions and labels
                    subset_scene = df_scene[[LABEL, TRACKER_ID, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD, RADIUS]]
                    origin = REFERENCE_POINT_3D
                    point_coordinates.insert(len(point_coordinates), origin)
                    # loop into other vehicles and check whether they are too close to the instrumented car
                    for i in range(len(subset_scene.index)):
                        label = subset_scene.loc[i, LABEL]
                        tracker_id = subset_scene.loc[i, TRACKER_ID]
                        object_position = np.array(
                            [subset_scene.loc[i, CENTER_X_COORD], subset_scene.loc[i, CENTER_Y_COORD],
                             subset_scene.loc[i, CENTER_Z_COORD]])
                        if object_position[0] < 0:  # the considered traffic participant is behind the instrumented
                            # car --> do not consider this object
                            continue
                        if IGNORE_3D:
                            object_position[2] = 0
                        point_coordinates.insert(len(point_coordinates), object_position)

                        distance_to_object_i = subset_scene.loc[
                            i, RADIUS]  # distance from a 'other vehicle' to instrumented car
                        # log alert when vehicles are too close to the instrumented car
                        if distance_to_object_i < minimal_distance:
                            log_alert('distance_checker v0', scenario, frame_id, label, tracker_id, minimal_distance,
                                      distance_to_object_i)
                    if plot:
                        # create plot and save it
                        context = "prototypeV0/"
                        path = PATH_DIR_REPORT_FIGURE + context + scenario
                        if not (os.path.exists(os.path.dirname(path))):
                            os.mkdir(os.path.dirname(path))
                        plot3DPoints(point_coordinates, save_plot=True, scenario_name=scenario, frame_name=frame_id,
                                     path=path)


if __name__ == '__main__':
    main()
