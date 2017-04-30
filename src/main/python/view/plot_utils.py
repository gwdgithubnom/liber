#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from context import resource_manager
import pandas
import numpy
from tools import logger
import numpy as np
import matplotlib.pyplot as plt

log = logger.getLogger()


def plot_image_file(img):
    plt.imshow(img)
    plt.show()


def plot_image(narray, w='', h=''):
    log.info("plot image array:" + str(narray.shape))
    if w is not '':
        narray = narray.reshape(w, h)
    plt.imshow(narray)
    plt.show()


def plot_rho_delta(rho, delta):
    '''
    Plot scatter diagram for rho-delta points

    Args:
        rho   : rho list
        delta : delta list
    '''
    log.info("PLOT: rho-delta plot")
    plot_scatter_diagram(0, rho[1:], delta[1:], x_label='rho', y_label='delta', title='rho-delta')


# def plot_scatter_diagram(which_fig, x, y, x_label='x', y_label='y', title='title', style_list=None):
#     '''
#     Plot scatter diagram
#
#     Args:
#         which_fig  : which sub plot
#         x          : x array
#         y          : y array
#         x_label    : label of x pixel
#         y_label    : label of y pixel
#         title      : title of the plot
#     '''
#     styles =
#     assert len(x) == len(y)
#     if style_list != None:
#         assert len(x) == len(style_list) and len(styles) >= len(set(style_list))
#     plt.figure(which_fig)
#     plt.clf()
#     if style_list == None:
#         plt.plot(x, y, styles[0])
#     else:
#         clses = set(style_list)
#         xs, ys = {}, {}
#         for i in range(len(x)):
#             try:
#                 xs[style_list[i]].append(x[i])
#                 ys[style_list[i]].append(y[i])
#             except KeyError:
#                 xs[style_list[i]] = [x[i]]
#                 ys[style_list[i]] = [y[i]]
#         added = 1
#         for idx, cls in enumerate(clses):
#             if cls == -1:
#                 style = styles[0]
#                 added = 0
#             else:
#                 style = styles[idx + added]
#             plt.plot(xs[cls], ys[cls], style)
#     plt.title(title)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.ylim(bottom=0)
#     plt.show()

def plot_dataframe_scatter_diagram(which_fig, data, x_label='x', y_label='y', title='title', label=None):
    styles = ['k.', 'g.', 'r.', 'c.', 'm.', 'y.', 'b.']
    linestyles = ['-.', '--', 'None', '-', ':']
    stylesMarker = markers = ['.',  # point
                              ',',  # pixel
                              'o',  # circle
                              'v',  # triangle down
                              '^',  # triangle up
                              '<',  # triangle_left
                              '>',  # triangle_right
                              '1',  # tri_down
                              '2',  # tri_up
                              '3',  # tri_left
                              '4',  # tri_right
                              '8',  # octagon
                              's',  # square
                              'p',  # pentagon
                              '*',  # star
                              'h',  # hexagon1
                              'H',  # hexagon2
                              '+',  # plus
                              'x',  # x
                              'D',  # diamond
                              'd',  # thin_diamond
                              '|',  # vline

                              ]
    # styles = []
    stylesColors = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "color.csv").ix[:,
                   2]
    plt.figure(which_fig)
    plt.clf()

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(bottom=0)
    plt.legend(loc='upper left')
    plt.show()


def plot_scatter_diagram(which_fig, x, y, x_label='x', y_label='y', title='title', label=None):
    '''
    Plot scatter diagram

    Args:
        which_fig  : which sub plot
        x          : x array
        y          : y array
        x_label    : label of x pixel
        y_label    : label of y pixel
        title      : title of the plot
    '''
    styles = ['k.', 'g.', 'r.', 'c.', 'm.', 'y.', 'b.']
    linestyles = ['-.', '--', 'None', '-', ':']
    stylesMarker = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "style.csv").ix[:,
                   3]

    stylesColors = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "style.csv").ix[:,
                   2]

    assert len(x) == len(y)
    if label != None:
        assert len(x) == len(label) # and len(stylesMarker) >= len(set(label))
    plt.figure(which_fig)
    plt.clf()
    if label == None:
        plt.plot(x, y, styles[0])
    else:
        l = len(label)
        labelSet = set(label)
        k = 0
        for i in labelSet:
            xs = []
            ys = []
            for j in range(l):
                if i == label[j]:
                    xs.append(x[j])
                    ys.append(y[j])
            k = k + 1
            try:
                   plt.scatter(xs, ys, c=stylesColors[k].strip(), marker=r"$ {} $".format(str(i)),label=i)
            except:
                log.fatal(stylesMarker)
                log.fatal(stylesColors)
                log.fatal(stylesMarker[k])
                log.fatal(stylesColors[k])
                plt.scatter(xs, ys, c=stylesColors[k].strip(), marker=r"$ {} $".format(str(i)),label=i)
                exit()

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(bottom=0)
    # plt.legend(loc='upper left')
    plt.show()



def save_scatter_diagram(which_fig, x, y, x_label='x', y_label='y', title='title', label=None,
                         path=resource_manager.Properties.getDefaultDataFold() + "result" + resource_manager.getSeparator() + "result.png"):
    '''
    Plot scatter diagram

    Args:
        which_fig  : which sub plot
        x          : x array
        y          : y array
        x_label    : label of x pixel
        y_label    : label of y pixel
        title      : title of the plot
    '''
    styles = ['k.', 'g.', 'r.', 'c.', 'm.', 'y.', 'b.']
    linestyles = ['-.', '--', 'None', '-', ':']
    stylesMarker = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "style.csv").ix[:,
                   3]

    stylesColors = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "style.csv").ix[:,
                   2]

    assert len(x) == len(y)
    if label != None:
        assert len(x) == len(label) # and len(stylesMarker) >= len(set(label))
    plt.figure(which_fig)
    plt.clf()
    if label == None:
        plt.plot(x, y, styles[0])
    else:
        l = len(label)
        labelSet = set(label)
        k = 0
        for i in labelSet:
            xs = []
            ys = []
            for j in range(l):
                if i == label[j]:
                    xs.append(x[j])
                    ys.append(y[j])
            k = k + 1
            try:
                if k<=7:
                    plt.scatter(xs, ys, c=stylesColors[k].strip(), marker=stylesMarker[k],label=i)
                else:
                    plt.scatter(xs, ys, c=stylesColors[k%100].strip(), marker=r"$ {} $".format(str(i)),label=i)
            except:
                log.fatal(stylesMarker)
                log.fatal(stylesColors)
                log.fatal(stylesMarker[k])
                log.fatal(stylesColors[k])
                plt.scatter(xs, ys, c=stylesColors[k].strip(), marker=r"$ {} $".format(str(i)),label=i)
                exit()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(bottom=0)
    plt.savefig(path,dpi=900)
    #plt.savefig(path)
    plt.close()


def save_all_scatter_diagram(which_fig, x, y, x_label='x', y_label='y', title='title', label=None,
                         path=resource_manager.Properties.getDefaultDataFold() + "result" + resource_manager.getSeparator() + "result.png"):
    '''
    Plot scatter diagram

    Args:
        which_fig  : which sub plot
        x          : x array
        y          : y array
        x_label    : label of x pixel
        y_label    : label of y pixel
        title      : title of the plot
    '''
    styles = ['k.', 'g.', 'r.', 'c.', 'm.', 'y.', 'b.']
    linestyles = ['-.', '--', 'None', '-', ':']
    stylesMarker = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "style.csv").ix[:,
                   3]

    stylesColors = pandas.read_csv(
        resource_manager.Properties.getDefaultDataFold() + "view" + resource_manager.getSeparator() + "style.csv").ix[:,
                   2]

    assert len(x) == len(y)
    if label != None:
        assert len(x) == len(label) # and len(stylesMarker) >= len(set(label))
    plt.figure(which_fig)
    plt.clf()
    if label == None:
        plt.plot(x, y, styles[0])
    else:
        l = len(label)
        labelSet = set(label)
        k = 0
        for i in labelSet:
            xs = []
            ys = []
            for j in range(l):
                if i == label[j]:
                    xs.append(x[j])
                    ys.append(y[j])
            k = k + 1
            try:
                # if k<=7:
                #     plt.scatter(xs, ys, c=stylesColors[k].strip(), marker=stylesMarker[k],label=i)
                # else:
                plt.scatter(xs, ys, c=stylesColors[k%100].strip(), marker=r"$ {} $".format(str(i)),label=i)
            except:
                log.fatal(stylesMarker)
                log.fatal(stylesColors)
                log.fatal(stylesMarker[k])
                log.fatal(stylesColors[k])
                plt.scatter(xs, ys, c=stylesColors[k].strip(), marker=r"$ {} $".format(str(i)),label=i)
                exit()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(bottom=0)
    # plt.legend(loc='upper left')
    plt.savefig(path+".jpg",dpi=900)
    #plt.savefig(path+".jpg")
    plt.close()


if __name__ == '__main__':
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([2, 3, 4, 5, 6, 2, 4, 8])
    cls = np.array([1, 4, 2, 3, 5, 1, 1, 7])
    plot_scatter_diagram(0, x, y, label=cls)
