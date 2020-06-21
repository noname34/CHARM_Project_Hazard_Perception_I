#!/user/bin/env python3
# -*- coding: utf-8 -*-
import fnmatch
import os

import pandas as pd

from configuration import PATH_DIR_RAW_DATA, PATH_DIR_INTERIM_DATA
from data.external.dataset_data_format import SPEED, TIMESTAMP, MEAN_SPEED, FRAME_DURATION, VELOCITY_FILES_PATTERN, \
    SCENARIO_DIR_PATTERN


def frame_mean_duration():
    incr=0
    total=0

    scenarios = os.listdir(PATH_DIR_INTERIM_DATA)
    scenarios.sort()
    for scenario in scenarios:
        print(PATH_DIR_RAW_DATA + scenario)
        if fnmatch.fnmatch(scenario, SCENARIO_DIR_PATTERN):
            filenames = os.listdir(PATH_DIR_INTERIM_DATA + scenario)
            filenames.sort()
            for filename in filenames:
                if fnmatch.fnmatch(filename, VELOCITY_FILES_PATTERN):
                    df = pd.read_csv(PATH_DIR_INTERIM_DATA + scenario + '/' + filename, float_precision="round_trip")
                    frame_dur=df.loc[0, FRAME_DURATION]
                    incr+=1
                    total+=frame_dur
                    #if frame_duration<0.089:
                    #print(frame_duration)
    total/=incr
    print(total)


frame_mean_duration()