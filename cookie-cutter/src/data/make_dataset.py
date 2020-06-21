#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception

from src.data.add_distance import add_distance_info
from src.data.labels_txt2csv import labels_txt_2_labels_csv
from src.data.mean_speed import mean_speed_sequence
from src.data.mean_velocity import mean_velocity_direction


def main():
    """
    This script takes only useful parts of information from /data/raw, manipulate them if necessary and store them to
    /data/interim. Features will then use data of /data/interim so that raw data are not modified at all.
    """
    labels_txt_2_labels_csv()  # transform labels_yyy.txt to labels_yyy.csv
    add_distance_info()  # calculate spherical coordinates and add them to labels_yyy.csv
    mean_speed_sequence()  # calculate the mean speed value of the ego car for each frame and store the information
    # in velocity files
    mean_velocity_direction()  # same but for the velocity vector


if __name__ == '__main__':
    main()
    print("make_dataset.py done")
