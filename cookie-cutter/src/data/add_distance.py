#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception

import fnmatch
import os

import pandas as pd

from configuration import PATH_DIR_INTERIM_DATA, PRECISION_FLOAT
from data.external.dataset_data_format import *
from src.libraries.myMathLib import cart2sph


def add_distance_info():
    """
    calculate spherical coordinates and add them to existing files that have name pattern labels_yyy.csv
    :return:
    """
    # list all scenarios and sort them alphabetically
    scenarios = os.listdir(PATH_DIR_INTERIM_DATA)
    scenarios.sort()
    for scenario in scenarios:
        print(PATH_DIR_INTERIM_DATA + scenario)
        if fnmatch.fnmatch(scenario, 'scenario_*'):
            filenames=os.listdir(PATH_DIR_INTERIM_DATA + scenario)
            filenames.sort()
            # search for label files
            for filename in filenames:
                if fnmatch.fnmatch(filename, LABEL_FILES_PATTERN):
                    # open label file for the frame and store it as structured data
                    df = pd.read_csv(PATH_DIR_INTERIM_DATA + scenario + '/' + filename, float_precision="round_trip")
                    print(PATH_DIR_INTERIM_DATA + scenario + '/' + filename)
                    # convert coordinates from cartesian system to spherical system
                    for i in range(len(df.index)):
                        object_centroid_cart = np.array([df.loc[i, CENTER_X_COORD], df.loc[i, CENTER_Y_COORD],
                                                         df.loc[i, CENTER_Z_COORD]])
                        object_centroid_sph = cart2sph(object_centroid_cart)
                        # add spherical coordinates to the pandas dataframe
                        df.loc[i, RADIUS] = round(object_centroid_sph[0], PRECISION_FLOAT)
                        df.loc[i, POLAR_ANGLE] = round(object_centroid_sph[1], PRECISION_FLOAT)
                        df.loc[i, AZIMUTH_ANGLE] = round(object_centroid_sph[2], PRECISION_FLOAT)
                        # and store the dataframe to the label file
                        df.to_csv(PATH_DIR_INTERIM_DATA + scenario + '/' + filename, index=False)
