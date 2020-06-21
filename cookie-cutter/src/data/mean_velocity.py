#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 03.04.2020
# Context: CHARM PROJECT - Harzard perception

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 03.04.2020
# Context: CHARM PROJECT - Harzard perception

import fnmatch
import os

import pandas as pd
import numpy as np

from configuration import PATH_DIR_RAW_DATA, PATH_DIR_INTERIM_DATA, PRECISION_FLOAT
from data.external.dataset_data_format import SPEED, TIMESTAMP, MEAN_SPEED, FRAME_DURATION, VELOCITY_FILES_PATTERN, \
    SCENARIO_DIR_PATTERN, VELOCITY_X, VELOCITY_Y, VELOCITY_Z, GPS_FILES_PATTERN


def mean_velocity_direction():
    # list all scenarios and parse them alphabetically
    scenarios = os.listdir(PATH_DIR_RAW_DATA)
    scenarios.sort()
    for scenario in scenarios:
        print(PATH_DIR_RAW_DATA + scenario)
        if fnmatch.fnmatch(scenario, SCENARIO_DIR_PATTERN):
            # create scenario_yyy if it does not exist
            if not (os.path.exists(PATH_DIR_INTERIM_DATA + scenario)):
                os.mkdir(PATH_DIR_INTERIM_DATA + scenario)
            # search for gps files
            filenames = os.listdir(PATH_DIR_RAW_DATA + scenario)
            filenames.sort()
            for filename in filenames:
                if fnmatch.fnmatch(filename, GPS_FILES_PATTERN):
                    # read gps file for the current frame and save the content as a structured data
                    df = pd.read_csv(PATH_DIR_RAW_DATA + scenario + '/' + filename, float_precision="round_trip")
                    v_x = 0
                    v_y = 0
                    v_z = 0
                    # calculate the mean value of each component of the velocity vector
                    for i in range(len(df.index)):
                        v_x += df.loc[i, VELOCITY_X]
                        v_y += df.loc[i, VELOCITY_Y]
                        v_z += df.loc[i, VELOCITY_Z]
                    velocity_vector = np.array([
                        round(v_x / float(len(df.index)), PRECISION_FLOAT),
                        round(v_y / float(len(df.index)), PRECISION_FLOAT),
                        round(v_z / float(len(df.index)), PRECISION_FLOAT)
                    ])
                    # store result (mean velocity vector for the frame)
                    data = {VELOCITY_X: [velocity_vector[0]],
                            VELOCITY_Y: [velocity_vector[1]],
                            VELOCITY_Z: [velocity_vector[2]],
                            }
                    print(velocity_vector)

                    # and save the information to the new csv file generated for interim data folder
                    new_df = pd.DataFrame(data, columns=[VELOCITY_X, VELOCITY_Y, VELOCITY_Z])
                    new_csv_file_path = PATH_DIR_INTERIM_DATA + (scenario + '/') + filename
                    print(new_csv_file_path)

                    new_df.to_csv(new_csv_file_path, index=False)