#!/user/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 29.04.20
# Context: CHARM PROJECT - Harzard perception

import cv2
import glob

from configuration import PATH_DIR_INTERIM_DATA, PATH_DIR_RAW_DATA, ROOT_DIR


def main():
    scenario = "scenario_002"
    img_array = []
    for filename in glob.glob(PATH_DIR_RAW_DATA + scenario + '/image_*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(ROOT_DIR + '/reports/output_video' + '/image_movie.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15,
                          size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()



    img_array = []
    for filename in glob.glob(ROOT_DIR + "/reports/figures/prototypeV1.1/" + scenario + '/frame_*'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(ROOT_DIR + '/reports/output_video' + '/plots_movie.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15,
                          size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


main()
print('done')
