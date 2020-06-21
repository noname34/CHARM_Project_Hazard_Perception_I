#!/user/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from configuration import PATH_DIR_INTERIM_DATA
from data.external.dataset_data_format import VELOCITY_FILES_PATTERN, SCENARIO_DIR_PATTERN
from src.libraries.myFileSystemLib import getNextFile, getFirstFileInDir


def main():
    path_at_i = getFirstFileInDir(PATH_DIR_INTERIM_DATA + "scenario_002", VELOCITY_FILES_PATTERN)
    print(path_at_i)
    nextFile = getNextFile(path_at_i, VELOCITY_FILES_PATTERN, SCENARIO_DIR_PATTERN, increment=10)
    print("nextFile: ", nextFile)


if __name__ == '__main__':
    main()