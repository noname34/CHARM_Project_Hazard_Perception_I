#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception


import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DIR_RAW_DATA = ROOT_DIR + '/data/raw/link_to_dataset/'
PATH_DIR_INTERIM_DATA = ROOT_DIR + '/data/interim/'
PATH_DIR_REPORT_FIGURE = ROOT_DIR + "/reports/figures/"
PATH_DIR_REPORT_ALERTS = ROOT_DIR + "/reports/alerts/"

IGNORE_3D = os.environ['IGNORE_3D']

ANTICIPATION_TIME = 0.9  # second
THRESHOLD_DISTANCE = 2  # meter

PRECISION_FLOAT = 4  # float precision when float operations are used
