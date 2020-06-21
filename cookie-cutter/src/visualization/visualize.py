#!/user/bin/env python3
# -*- coding: utf-8 -*-


# @Author: Kevin Bürgisser
# @Email: kevin.buergisser@edu.hefr.ch
# @Date: 04.2020
# Context: CHARM PROJECT - Harzard perception


import os
import matplotlib.pyplot as plt
from configuration import PATH_DIR_REPORT_FIGURE


def plot3DLines(list_of_lines, multiple_subplots=False, save_plot=False, format='png', show=False, **kwargs):
    """
    Method to plot 3D straight lines.
    :param list_of_lines: [list] that contains all points to plot
    :param multiple_subplots: Boolean. Yes=make subplots
    :param save_plot: Boolean. Yes=save plot in path (path is given in kwargs)
    :param show: Boolean. Yes=show plot
    :param format: string. Format of the image to save. Default is 'png'
    :param kwargs:
        frame_name
        scenario_name
        path
    :return:
    """
    colors = {
        0: 'blue',
        1: 'green',
        2: 'red'
    }
    if 'color_a' in kwargs:
        colors['color_a'] = kwargs.get('color_a')
    if 'color_b' in kwargs:
        colors['color_b'] = kwargs.get('color_b')
    if 'color_d' in kwargs:
        colors['color_d'] = kwargs.get('color_d')

    number_points = len(list_of_lines)
    number_of_trajectories = number_points // 2

    if multiple_subplots:
        fig = plt.figure(figsize=plt.figaspect(0.5))
        index = 1
        for i in range(0, number_points, 2):
            ax = fig.add_subplot(1, number_of_trajectories, index, projection='3d')
            if i + 1 >= number_points:
                break
            ax.plot([list_of_lines[i + 1][0], list_of_lines[i][0]], [list_of_lines[i + 1][1], list_of_lines[i][1]],
                    zs=[list_of_lines[i + 1][2], list_of_lines[i][2]],
                    color=colors.get(i // 2 % number_of_trajectories))
            index += 1

    else:
        ax = plt.axes(projection='3d')
        marker = False
        for i in range(0, number_points, 2):
            marker = not marker
            if i + 1 >= number_points:
                break
            ax.plot([list_of_lines[i + 1][0], list_of_lines[i][0]], [list_of_lines[i + 1][1], list_of_lines[i][1]],
                    zs=[list_of_lines[i + 1][2], list_of_lines[i][2]],
                    color=colors.get(i // 2 % number_of_trajectories), marker="o", markevery=[0])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    frame_name = ""
    if 'frame_name' in kwargs and 'scenario_name' in kwargs:
        frame_name = "frame_" + kwargs.get('frame_name')
        scenario_name = kwargs.get('scenario_name')
        plt.title("Trajectories prediction, scenario :  " + scenario_name + " " + frame_name)
    if save_plot:
        if 'path' in kwargs:
            path = kwargs.get('path')
        else:
            path = PATH_DIR_REPORT_FIGURE + "markeroutput/"
        if not (os.path.exists(path)):
            os.mkdir(path)
        plt.savefig(path + "/" + frame_name, format=format, bbox_inches='tight')
    if show:
        plt.show()


def plot3DPoints(list_of_points, save_plot=False, format='png', show=False, **kwargs):
    """
    Method that plot a list of points given in parameter
    :param list_of_lines: [list] that contains all points to plot
    :param save_plot: Boolean. Yes=save plot in path (path is given in kwargs)
    :param format: string. Format of the image to save. Default is 'png'
    :param show: Boolean. Show plot
    :param kwargs:
        frame_name
        scenario_name
        path
    :return:
    """

    number_points = len(list_of_points)

    colors = {
        0: 'blue',
        1: 'green',
        2: 'red'
    }
    if 'color_a' in kwargs:
        colors['color_a'] = kwargs.get('color_a')
    if 'color_b' in kwargs:
        colors['color_b'] = kwargs.get('color_b')
    if 'color_d' in kwargs:
        colors['color_d'] = kwargs.get('color_d')

    ax = plt.axes(projection='3d')
    marker = False
    for i in range(0, number_points, 1):
        marker = not marker
        if i + 1 >= number_points:
            break
        ax.plot(xs=[list_of_points[i][0], 0], ys=[list_of_points[i][1], 0], zs=[list_of_points[i][2], 0],
                color=colors.get(i // 2 % number_points), marker="o", markevery=[0])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    frame_name = ""
    if 'frame_name' in kwargs and 'scenario_name' in kwargs:
        frame_name = "frame_" + kwargs.get('frame_name')
        scenario_name = kwargs.get('scenario_name')
        plt.title("Trajectories prediction, scenario :  " + scenario_name + " " + frame_name)
    if save_plot:
        if 'path' in kwargs:
            path = kwargs.get('path')
        else:
            path = PATH_DIR_REPORT_FIGURE + "output/"
        if not (os.path.exists(path)):
            os.mkdir(path)
        plt.savefig(path + "/" + frame_name, format=format, bbox_inches='tight')
    if show:
        plt.show()
