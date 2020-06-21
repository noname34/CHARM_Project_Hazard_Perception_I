#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception

import unittest

from configuration import PATH_DIR_INTERIM_DATA
from data.external.dataset_data_format import SCENARIO_DIR_PATTERN, LABEL_FILES_PATTERN
from src.libraries.myFileSystemLib import getNextFolder, getNextFile, getFirstFileInDir


class TextGetNextFolder(unittest.TestCase):
    """
    Class to test methods related to files manipulation in the file system
    """
    def test_getNextFolder(self):
        scenario = "scenario_002"
        filename = "labels_3d1_000.csv"
        path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
        self.assertEqual(getNextFolder(path, SCENARIO_DIR_PATTERN), PATH_DIR_INTERIM_DATA + "scenario_003")

        scenario = "scenario_443"
        filename = "labels_3d1_243.csv"
        path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
        self.assertEqual(getNextFolder(path, SCENARIO_DIR_PATTERN), "")

    def test_getNextFile(self):
        scenario = "scenario_002"
        filename = "labels_3d1_000.csv"
        path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
        self.assertEqual(getNextFile(path, LABEL_FILES_PATTERN, SCENARIO_DIR_PATTERN),
                         PATH_DIR_INTERIM_DATA + scenario + "/labels_3d1_001.csv")

        scenario = "scenario_002"
        filename = "labels_3d1_243.csv"
        path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
        self.assertEqual(getNextFile(path, LABEL_FILES_PATTERN, SCENARIO_DIR_PATTERN),
                         PATH_DIR_INTERIM_DATA + "scenario_003/labels_3d1_000.csv")

        scenario = "scenario_443"
        filename = "labels_3d1_242.csv"
        path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
        self.assertEqual(getNextFile(path, LABEL_FILES_PATTERN, SCENARIO_DIR_PATTERN),
                         PATH_DIR_INTERIM_DATA + scenario + "/labels_3d1_243.csv")

        scenario = "scenario_443"
        filename = "labels_3d1_243.csv"
        path = PATH_DIR_INTERIM_DATA + scenario + '/' + filename
        self.assertEqual(getNextFolder(path, SCENARIO_DIR_PATTERN), "")

    def test_getFirstFileInDir(self):
        scenario = "scenario_443"
        self.assertEqual(getFirstFileInDir(PATH_DIR_INTERIM_DATA + scenario, LABEL_FILES_PATTERN),
                         PATH_DIR_INTERIM_DATA + scenario + "/labels_3d1_000.csv")


if __name__ == '__main__':
    unittest.main()
    print("all tests passed")
