#!/user/bin/env python3
# -*- coding: utf-8 -*-
import csv
import fnmatch
import os
from datetime import datetime

from configuration import PATH_DIR_REPORT_ALERTS


def getNextFolder(currentFolderPath, pattern):
    """This function returns the path of the folder that directly follows (alphabetically and at the same level) a given
    folder having a specific name pattern

    This method receives the path of a folder called currentFolderPath and has to return the following alphabetically
    folder that is at the same level as the current folder and has the same pattern name. If no folder is found,
    e.g currentFolderPath is the very last folder of the hierarchy (with the given pattern name), the function return an
    empty string.

    Parameters
    ----------
    currentFolderPath : string
        Path of the current folder in the system
    pattern : string
        Folder pattern in the file system. For example:  "scenario_*" to say that the folder name could be
        "scenario_000", "scenario_234" or whatever

    Returns
    -------
    string
        Path of the folder that directly follows currentFolderPath alphabetically
        Note: In the case, no folder has been found, returns an empty string

    Raises
    ------
    FileNotFoundError or NotADirectoryError
        Access to an unknown folder. Directly handled by returning an empty string

    Examples
    --------
    Given a dir tree with the following folders:
    home/
    ----- scenario_441
    ----- scenario_443
    getNextFolder(home/scenario_441) returns scenario_443 whereas getNextFolder(home/scenario_443) returns ""
    """

    # when folderFound has been set to True, it means that the folder that follows currentFolderPath within the basePath
    # tree has been found and therefore the method has to return its path
    folderFound = False

    try:
        # if currentFolder is a file of expected currentFolder, get parent folder name
        if not os.path.isdir(currentFolderPath):
            currentFolderPath = os.path.dirname(currentFolderPath)

        # get global path (without the pattern). For example /home/interim/scenario_002 becomes /home/interim
        # currentFolder = basePath + folderName
        folderName = os.path.basename(currentFolderPath)
        basePath = os.path.dirname(currentFolderPath)

        p = os.listdir(basePath)
        p.sort()
        for i in p:
            if folderFound:
                return basePath + '/' + i

            if basePath + '/' + i == currentFolderPath:
                if fnmatch.fnmatch(folderName, pattern):
                    folderFound = True
                else:
                    return ""
        # nothing has been found
        return ""
    except FileNotFoundError or NotADirectoryError:
        return ""


def getFirstFileInDir(dirPath, filePattern):
    try:
        files = os.listdir(dirPath)
        files.sort()
        for i in files:
            if fnmatch.fnmatch(os.path.basename(dirPath + '/' + i), filePattern):
                return dirPath + '/' + i
        return ""

    except FileNotFoundError or NotADirectoryError:
        return ""


def getNextFile(currentFilePath, filePattern, parentPattern, increment=1):
    """This method gives the path of the file that directly follows a given file with a specific pattern.

    Parameters
    ----------
    :param increment: get increment-th frame that follows the current file
    :param currentFilePath: string
        Path of the current file we want to find the very following file
    :param filePattern: string
        Name pattern of the file
    :param parentPattern: string
        Name pattern of the parent folder the current file is in. This parameter is useful when the given file is the
        last file of a folder
        For example: the parent folder of the file text.txt is something like "ThisIsAFolder_*"
        ThisIsAFolder_012
            --- text.txt

    Returns
    -------
    string
        Path of the file that directly follows currentFilePath alphabetically
        Note: In the case, no file has been found, returns an empty string

    Raises
    ------
    FileNotFoundError or NotADirectoryError
        Access to an unknown file. Directly handled by returning an empty string

    Examples
    --------
    scenario_002
        --- CAN_vel_000.csv
        --- CAN_vel_001.csv
        ...
        ---CAN_vel_238.csv
    scenario_003
        --- CAN_vel_000.csv
    ...


    getNextFile("/home/scenario_002/CAN_vel_000.csv", "CAN_vel_*.csv", "scenario_*")
        returns "/home/scenario_002/CAN_vel_001.csv"
    getNextFile("/home/scenario_002/CAN_vel_238.csv", "CAN_vel_*.csv", "scenario_*") returns CAN_vel_001.csv
        returns "/home/scenario_003/CAN_vel_000.csv"
    """

    try:
        # when fileFound has been set to True, it means that the file that follows fileFound within the basePath
        # tree has been found and therefore the method has to return its path
        currentFileFound = False

        increment = int(increment)
        increment -= 1  # increment-1 to 0

        # get global path (without the pattern). For example /home/interim/scenario_002/file.txt becomes
        # /home/interim currentFilePath = basePath + folderName
        fileName = os.path.basename(currentFilePath)
        basePath = os.path.dirname(currentFilePath)

        p = os.listdir(basePath)
        p.sort()
        for i in p:
            # look for increment-th file after current file

            if currentFileFound:
                if increment == 0:
                    return basePath + '/' + i
                increment -= 1
                continue

            # look for current file
            if basePath + '/' + i == currentFilePath:
                if fnmatch.fnmatch(fileName, filePattern):
                    currentFileFound = True
                    continue
                else:
                    return ""

        # the method did not found next file of currentFilePath within the directory basePath. So let's jump to the next
        # folder (but only if we are not already in the last directory!)
        nextFolder = getNextFolder(basePath, parentPattern)
        if nextFolder != "":
            nextFile = getFirstFileInDir(nextFolder, filePattern)
            if nextFile != "":
                return nextFile

        return ""
        # nothing has been found

    except FileNotFoundError or NotADirectoryError:
        return ""


def log_alert(feature, scenario, frame, label, ID_TRACKER, value_expected, value_mesured):
    path = PATH_DIR_REPORT_ALERTS + feature + '.csv'
    line = []
    with open(path, 'a+', newline='') as file:
        if os.path.getsize(path) == 0:
            init_alert_file(path, 'time', 'feature', 'scenario', 'frame', 'label', 'ID_tracker', 'value_expected',
                            'value_measured')
        writer = csv.writer(file)
        line.insert(len(line), datetime.now())
        line.insert(len(line), feature)
        line.insert(len(line), scenario)
        line.insert(len(line), frame)
        line.insert(len(line), label)
        line.insert(len(line), ID_TRACKER)
        line.insert(len(line), value_expected)
        line.insert(len(line), value_mesured)
        writer.writerow(line)


def init_alert_file(path, *args):
    if path == "" or len(args) == 0:
        return
    line = []
    with open(path, 'w+', newline='') as file:
        writer = csv.writer(file)
        for arg in args:
            line.insert(len(line), arg)
        writer.writerow(line)
