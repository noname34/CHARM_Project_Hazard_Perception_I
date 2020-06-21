#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 03.04.2020
# Context: CHARM PROJECT - Harzard perception

import fnmatch
import os
import pandas as pd

from configuration import PATH_DIR_RAW_DATA, PATH_DIR_INTERIM_DATA
from data.external.dataset_data_format import *

column_labels = np.array(
    [LABEL, TRACKER_ID, STATE, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD, LENGTH_X_COORD, LENGTH_Y_COORD,
     LENGTH_Z_COORD, YAW])


def txt2csv(txt_path, csv_path, pattern):
    read_file = pd.read_csv(txt_path, header=None, float_precision="round_trip")
    read_file.columns = pattern
    read_file.to_csv(csv_path, index=None)


def labels_txt_2_labels_csv():
    """
    transform labels_yyy.txt to labels_yyy.csv
    :return:
    """
    # list all scenarios within raw data folder and sort them alphabetically
    scenarios = os.listdir(PATH_DIR_RAW_DATA)
    scenarios.sort()
    for scenario in scenarios:
        print(PATH_DIR_RAW_DATA + scenario)
        if fnmatch.fnmatch(scenario, SCENARIO_DIR_PATTERN):
            # create folder scenario_yyy if it does not exist
            if not (os.path.exists(PATH_DIR_INTERIM_DATA + scenario)):
                os.mkdir(PATH_DIR_INTERIM_DATA + scenario)
            # list all files within scenario_yyy
            filenames = os.listdir(PATH_DIR_RAW_DATA + scenario)
            filenames.sort()
            for filename in filenames:
                if fnmatch.fnmatch(filename, LABEL_FILES_PATTERN):
                    txt_file_path = PATH_DIR_RAW_DATA + scenario + '/' + filename
                    print(txt_file_path)
                    # crate new path for csv file we want to create
                    new_csv_file_path = PATH_DIR_INTERIM_DATA + (scenario + '/') + (
                        os.path.splitext(filename)[0]) + '.csv'
                    print(new_csv_file_path)
                    # convert txt file into csv file
                    txt2csv(txt_file_path, new_csv_file_path, column_labels)
