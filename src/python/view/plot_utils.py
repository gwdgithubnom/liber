#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tools import logger
import numpy as np
import matplotlib.pyplot as plt

log = logger.getLogger()


def plot_image(narray,w='',h='' ):
    log.info("plot image array:"+str(narray.shape))
    if w is not '':
        narray = narray.reshape(w,h)
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


def plot_scatter_diagram(which_fig, x, y, x_label='x', y_label='y', title='title', style_list=None):
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
    assert len(x) == len(y)
    if style_list != None:
        assert len(x) == len(style_list) and len(styles) >= len(set(style_list))
    plt.figure(which_fig)
    plt.clf()
    if style_list == None:
        plt.plot(x, y, styles[0])
    else:
        clses = set(style_list)
        xs, ys = {}, {}
        for i in range(len(x)):
            try:
                xs[style_list[i]].append(x[i])
                ys[style_list[i]].append(y[i])
            except KeyError:
                xs[style_list[i]] = [x[i]]
                ys[style_list[i]] = [y[i]]
        added = 1
        for idx, cls in enumerate(clses):
            if cls == -1:
                style = styles[0]
                added = 0
            else:
                style = styles[idx + added]
            plt.plot(xs[cls], ys[cls], style)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(bottom=0)
    plt.show()

def plot_scatter_diagram(which_fig, x, y, x_label='x', y_label='y', title='title', style_list=None):
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
    assert len(x) == len(y)
    if style_list != None:
        assert len(x) == len(style_list) and len(styles) >= len(set(style_list))
    plt.figure(which_fig)
    plt.clf()
    if style_list == None:
        plt.plot(x, y, styles[0])
    else:
        clses = set(style_list)
        xs, ys = {}, {}
        for i in range(len(x)):
            try:
                xs[style_list[i]].append(x[i])
                ys[style_list[i]].append(y[i])
            except KeyError:
                xs[style_list[i]] = [x[i]]
                ys[style_list[i]] = [y[i]]
        added = 1
        for idx, cls in enumerate(clses):
            if cls == -1:
                style = styles[0]
                added = 0
            else:
                style = styles[idx + added]
            plt.plot(xs[cls], ys[cls], style)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(bottom=0)
    plt.show()


if __name__ == '__main__':
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 7, 7])
    y = np.array([2, 3, 4, 5, 6, 2, 4, 8, 5, 6])
    cls = np.array([1, 4, 2, 3, 5, -1, -1, 6, 6, 6])
    plot_scatter_diagram(0, x, y, style_list=cls)
