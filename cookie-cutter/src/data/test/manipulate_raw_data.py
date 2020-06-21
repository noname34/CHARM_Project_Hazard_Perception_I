#!/user/bin/env python3
# -*- coding: utf-8 -*-


# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception

import numpy as np
import pandas as pd

from data.external.dataset_data_format import *

column_labels = np.array(
    [LABEL, TRACKER_ID, STATE, CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD, LENGTH_X_COORD, LENGTH_Y_COORD,
     LENGTH_Z_COORD, YAW])


def txt2csv(txt_path, csv_path, pattern):
    read_file = pd.read_csv(txt_path, header=None)
    read_file.columns = pattern
    read_file.to_csv(csv_path, index=None)


def main():
    """
    TEST SCRIPT
    This script takes only useful parts of information from /data/raw, manipulate them if necessary and store them to
    /data/interim. Features will then use data of /data/interim so that raw data are not modified at all.
    """
    txt2csv(r'../../../data/src/labels_3d1_000.txt', r'../../data/src/labels_3d1_000.csv', column_labels)
    df = pd.read_csv('../../../data/src/labels_3d1_000.csv')
    # print(df)
    subset = df[[CENTER_X_COORD, CENTER_Y_COORD, CENTER_Z_COORD]]
    print(subset)
    # print(subset.info())
    print(len(subset.index))  # number of rows


if __name__ == '__main__':
    main()
