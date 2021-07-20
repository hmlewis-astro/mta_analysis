#!/usr/bin/env python
# coding: utf-8


import os
import glob

# import data analysis, plotting packages
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set default plot params
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['figure.titlesize'] = 22
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["font.sans-serif"] = 'Tahoma'



def plot_grad(df_param, cmap, ax):
    '''Create a gradient colorbar

    df_param: pandas series
        Parameter to set the min/max values for the colorbar
    cmap: string
        Colormap to use in the colorbar
    ax: matplotlib.axes
		Axis to attach the colorbar to
    '''

    x_1, y_1 = (np.min(df_param),1.0)
    x_2, y_2 = (np.max(df_param),1.0)

    X = np.linspace(x_1, x_2, len(df_param))
    Xs = X[:-1]
    Xf = X[1:]
    Xpairs = zip(Xs, Xf)

    Y = np.linspace(y_1, y_2, len(df_param))
    Ys = Y[:-1]
    Yf = Y[1:]
    Ypairs = zip(Ys, Yf)

    C = np.linspace(0., 1., len(df_param))
    cmap = plt.get_cmap(cmap)

    for x, y, c in zip(Xpairs, Ypairs, C):
        ax.plot(x, y, c=cmap(c), linewidth=20.0)



def proc_map_files(map_file):
    df = gpd.read_file(map_file)
    print(df)
    df['median'] = df['median'].astype(np.float64) # Median temp in census tract

    return df

path = os.getcwd()
maps_path = path + '/heat_data/data/output/analysis_out/final/'
plot_path = path + '/plots/'
file_extn = '.geojson'

assert os.path.exists(maps_path), "Directory containing the final .geojson files missing!"

if not os.path.exists(plot_path):
    os.makedirs(plot_path)

map_files = glob.glob(maps_path + '/*' + file_extn)

for m in map_files:
    print(m)
    df = proc_map_files(m)
