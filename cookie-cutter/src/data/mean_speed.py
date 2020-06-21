#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception

import fnmatch
import os
import pandas as pd

from configuration import PATH_DIR_RAW_DATA, PATH_DIR_INTERIM_DATA, PRECISION_FLOAT
from data.external.dataset_data_format import SPEED, TIMESTAMP, MEAN_SPEED, FRAME_DURATION, VELOCITY_FILES_PATTERN, \
    SCENARIO_DIR_PATTERN


def mean_speed_sequence():
    """
    Calculate the mean speed value of the ego car for each frame and store the information
    :return:
    """
    # list all scenarios and parse them alphabetically
    scenarios = os.listdir(PATH_DIR_RAW_DATA)
    scenarios.sort()
    for scenario in scenarios:
        print(PATH_DIR_RAW_DATA + scenario)
        if fnmatch.fnmatch(scenario, SCENARIO_DIR_PATTERN):
            # create scenario_yyy dir if it does not exist
            if not (os.path.exists(PATH_DIR_INTERIM_DATA + scenario)):
                os.mkdir(PATH_DIR_INTERIM_DATA + scenario)
            filenames = os.listdir(PATH_DIR_RAW_DATA + scenario)
            filenames.sort()
            for filename in filenames:
                # look for files containing speed information
                if fnmatch.fnmatch(filename, VELOCITY_FILES_PATTERN):
                    df = pd.read_csv(PATH_DIR_RAW_DATA + scenario + '/' + filename, float_precision="round_trip")
                    mean_speed = 0
                    # compute mean speed
                    for i in range(len(df.index)):
                        mean_speed += df.loc[i, SPEED]
                    mean_speed = round(mean_speed / float(len(df.index)), 3)
                    new_df = pd.DataFrame({MEAN_SPEED: [mean_speed]})
                    new_csv_file_path = PATH_DIR_INTERIM_DATA + (scenario + '/') + filename
                    print(new_csv_file_path)

                    # calculate frame duration
                    new_df[FRAME_DURATION] = round(df.loc[len(df.index) - 1, TIMESTAMP] - df.loc[0, TIMESTAMP],PRECISION_FLOAT)
                    new_df.to_csv(new_csv_file_path, index=False)
