#!/usr/bin/env python
# coding: utf-8


import os
import glob

# import data analysis, plotting packages
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point
from tqdm import tqdm

# set default plot params
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['figure.titlesize'] = 22
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["font.sans-serif"] = 'Tahoma'



path = os.getcwd()
#TODO: uncomment these in final code version, and delete the maps_path below
#maps_path = path + '/heat_data/data/output/analysis_out/final/'
maps_path = path + '/data/output/analysis_out/final/'
plot_path = path + '/data/output/analysis_out/final/plots/'
file_extn = '.geojson'

# make sure that the map file exists
assert os.path.exists(maps_path), "Directory containing the final .geojson files missing!"

# make a new directory for the output plots
if not os.path.exists(plot_path):
    os.makedirs(plot_path)

# location of map file
map_file = maps_path + 'new-york' + file_extn

# read in geojson map file as a geopandas df
heat_df = gpd.read_file(map_file)

# convert median temperature in each Census block from Kelvin to Fahrenheit
heat_df['median'] = (heat_df['median'].astype(np.float64) - 273.15) \
                    * (9.0/5.0) + 32.0

# replace temperature outliers with the 0.5/99.9 percentile values
low_lim_temp = np.percentile(heat_df['median'],0.5)
up_lim_temp = np.percentile(heat_df['median'],99.9)
heat_df['median'].values[heat_df['median'].values < low_lim_temp] = low_lim_temp
heat_df['median'].values[heat_df['median'].values > up_lim_temp] = up_lim_temp



# plot temperature data
print('\nCreating temperature map...\n')
fig, ax = plt.subplots(2,1, figsize=(10,8),
                       gridspec_kw={'height_ratios': [20,1]})

# plot median temp in each Census block, bluer colors are cooler
heat_df.plot(column=heat_df['median'],
                  cmap='Spectral_r',
                  ax=ax[0])
ax[0].axis('off')
ax[0].set_title('Surface Temperature\n(relative to median)', fontsize=24)

# create the custom colorbar and add labels
min_temp = np.min(heat_df['median'])
max_temp = np.max(heat_df['median'])
median_temp = np.median(heat_df['median'])
range_temp = np.arange(min_temp,max_temp+0.05,0.05)

ax[1].scatter(range_temp, np.ones(len(range_temp)),
              c=range_temp, cmap='Spectral_r',
              s=50, marker='|')
ax[1].axis('off')
ax[1].text(min_temp,0.25,
             '{0:.1f}$^\circ$C\ncooler'.format(min_temp-median_temp),
             ha='center', fontsize=18)
ax[1].text(max_temp,0.25,
             '{0:.1f}$^\circ$C\nhotter'.format(max_temp-median_temp),
             ha='center', fontsize=18)

# save figure
plt.savefig(plot_path + '/new-york-temperature-data.png', dpi=300)
plt.close()



# scale the median temperature in each Census block from 1 to 10 (10 being the
# hottest, 1 being the coolest)
heat_df['HEAT_INDEX'] = heat_df['median'].apply(lambda x: 1.0 + 9.0 * (x-min_temp) / (max_temp-min_temp))
heat_df['HEAT_INDEX'].values[heat_df['HEAT_INDEX'].values > 10.0] = 10.0
heat_df['HEAT_INDEX'].values[heat_df['HEAT_INDEX'].values < 1.0] = 1.0



print('\nCreating heat index map...\n')
# plot heat index
fig, ax = plt.subplots(2,1, figsize=(10,8), gridspec_kw={'height_ratios': [20,1]})

# plot heat index in each Census block, bluer colors are lower heat index
heat_df.plot(column=heat_df['HEAT_INDEX'],
                  cmap='Spectral_r',
                  ax=ax[0])
ax[0].axis('off')
ax[0].set_title('Heat Index', fontsize=24)

# create the custom colorbar and add labels
range_index = np.arange(1.0,10.0+0.01,0.01)

ax[1].scatter(range_index, np.ones(len(range_index)), c=range_index, cmap='Spectral_r', s=50, marker='|')
ax[1].axis('off')
ax[1].text(1.0,0.25,
             'heat index\n1',
             ha='center', fontsize=18)
ax[1].text(10.0,0.25,
             'heat index\n10',
             ha='center', fontsize=18)

# save figure
plt.savefig(plot_path + '/new-york-heat-index.png', dpi=300)
plt.close()



# read in the analyzed MTA data file
#mta_df = pd.read_csv('mta_data_analyzed.csv')
mta_df = pd.read_csv('/Users/Hannah/Code/Metis/projects/mta_analysis/mta_data_analyzed.csv')



# create a mask to only show stations in NY (i.e., not NJ)
NJ_mask = (mta_df['LON'] < -74.02) & (mta_df['LAT'] > 40.70)

# plot entries data
print('\nCreating net entries map...\n')
fig, ax = plt.subplots(2,1, figsize=(10,8), gridspec_kw={'height_ratios': [20,1]})

# plot net entries for each station, bluer colors are fewer entries
heat_df.plot(edgecolor='k',color='none',linewidth=0.1,
             ax=ax[0])
ax[0].scatter(mta_df['LON'][~NJ_mask], mta_df['LAT'][~NJ_mask], s=20, alpha=0.8, c=mta_df['NET_ENTRIES'][~NJ_mask], cmap='Spectral_r', norm=matplotlib.colors.LogNorm())
ax[0].axis('off')
ax[0].set_title('Net Entries', fontsize=24)

# create the custom colorbar and add labels
min_entries = np.min(mta_df['NET_ENTRIES'])
max_entries = np.max(mta_df['NET_ENTRIES'])
median_entries = np.median(mta_df['NET_ENTRIES'])
range_entries = np.arange(min_entries,max_entries+10.0,10.0)

ax[1].scatter(range_entries, np.ones(len(range_entries)), c=range_entries, cmap='Spectral_r', s=50, marker='|')
ax[1].axis('off')
ax[1].text(min_entries,0.25,
             '{0:.0f} entries'.format(min_entries),
             ha='center', fontsize=18)
ax[1].text(max_entries,0.25,
             '{0:.0f} entries'.format(max_entries),
             ha='center', fontsize=18)

# save figure
plt.savefig(plot_path + '/new-york-station-net-entries.png', dpi=300)
plt.close()



print('\nCreating crowd index map...\n')
fig, ax = plt.subplots(2,1, figsize=(10,8), gridspec_kw={'height_ratios': [20,1]})

# plot crowd index for each station, bluer colors are lower crowd index
heat_df.plot(edgecolor='k',color='none',linewidth=0.1,
             ax=ax[0])
ax[0].scatter(mta_df['LON'][~NJ_mask], mta_df['LAT'][~NJ_mask], s=20, alpha=0.8, c=mta_df['CROWD_INDEX'][~NJ_mask], cmap='Spectral_r')
ax[0].axis('off')
ax[0].set_title('Crowd Index', fontsize=24)

# create the custom colorbar and add labels
range_index = np.arange(1.0,10.0+0.01,0.01)

ax[1].scatter(range_index, np.ones(len(range_index)), c=range_index, cmap='Spectral_r', s=50, marker='|')
ax[1].axis('off')
ax[1].text(1.0,0.25,
             'crowd index\n1',
             ha='center', fontsize=18)
ax[1].text(10.0,0.25,
             'crowd index\n10',
             ha='center', fontsize=18)

# save figure
plt.savefig(plot_path + '/new-york-station-crowd-index.png', dpi=300)
plt.close()



print('\nCombining the heat and crowd indices...\n')

med_temp_array = [-9999] * len(mta_df)
heat_index_array = [-9999] * len(mta_df)

# match dataframes based on which block each station is located within
# include a progress bar because this takes a while...
for i, row in tqdm(mta_df.iterrows(), total=mta_df.shape[0]):
    point = Point(row['LON'], row['LAT'])
    for j, block in heat_df.iterrows():
        geo = block.geometry
        if not isinstance(geo, float) and (point.within(geo) or point.intersects(geo)) and (med_temp_array[i] == -9999):
            med_temp_array[i] = block['median']
            heat_index_array[i] = block['HEAT_INDEX']
            break

# add columns to store the median temperature and heat index for each station
mta_df['MED_TEMP'] = med_temp_array
mta_df['HEAT_INDEX'] = heat_index_array

min_heat_index = np.min(heat_df['HEAT_INDEX'])
max_heat_index = np.max(heat_df['HEAT_INDEX'])
heat_df['HEAT_INDEX'] = heat_df['HEAT_INDEX'].apply(lambda x: 1.0 + 9.0 * (x-min_heat_index) / (max_heat_index-min_heat_index))
heat_df['HEAT_INDEX'].values[heat_df['HEAT_INDEX'].values > 10.0] = 10.0
heat_df['HEAT_INDEX'].values[heat_df['HEAT_INDEX'].values < 1.0] = 1.0

# save final combined dataframe
# if saved file already exisits, delete
if os.path.exists('mta_heat_data_analyzed.csv'):
    os.remove('mta_heat_data_analyzed.csv')

mta_df.to_csv('mta_heat_data_analyzed.csv')
