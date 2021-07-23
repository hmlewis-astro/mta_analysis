#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


import os
import glob

# import data analysis, plotting packages
import geopandas as gpd
from geopy import distance
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

# read in the analyzed MTA data file
mta_df = pd.read_csv('mta_heat_data_analyzed.csv')

# create a mask to only show stations in NY (i.e., not NJ)
NJ_mask = (mta_df['LON'] < -74.02) & (mta_df['LAT'] > 40.70)
mta_df = mta_df[~NJ_mask]

#mta_df = mta_df[mta_df['HEAT_INDEX'] != -9999]
# remove 'Unnamed' columns from the dataframe
mta_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)

print('\nCreating heat index station map...\n')
fig, ax = plt.subplots(2,1, figsize=(10,8), gridspec_kw={'height_ratios': [20,1]})

# plot heat index for each station, bluer colors are lower heat index
heat_df.plot(edgecolor='k',color='none',linewidth=0.1,
             ax=ax[0])
ax[0].scatter(mta_df['LON'], mta_df['LAT'], s=20, alpha=0.8, c=mta_df['HEAT_INDEX'], cmap='Spectral_r')
ax[0].axis('off')
ax[0].set_title('Heat Index (per station)', fontsize=24)

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
plt.savefig(plot_path + '/new-york-station-heat-index.png', dpi=300)
plt.close()

def risk_index(heat, crowd):
    return np.sqrt(0.65 * heat**2.0 + 0.35 * crowd**2.0)

mta_df['RISK_INDEX'] = mta_df.apply(lambda x: risk_index(x['HEAT_INDEX'], x['CROWD_INDEX']), axis=1)
low_lim_risk = np.percentile(mta_df['RISK_INDEX'],1.0)
mta_df['RISK_INDEX'].values[mta_df['RISK_INDEX'].values < low_lim_risk] = low_lim_risk

min_risk = np.min(mta_df['RISK_INDEX'])
max_risk = np.max(mta_df['RISK_INDEX'])

mta_df['RISK_INDEX'] = mta_df['RISK_INDEX'].apply(lambda x: (1.0 + 9.0 * (x-min_risk) / (max_risk-min_risk)).round(1))
mta_df['RISK_INDEX'].values[mta_df['RISK_INDEX'].values > 10.0] = 10.0
mta_df['RISK_INDEX'].values[mta_df['RISK_INDEX'].values < 1.0] = 1.0

plt.scatter(mta_df['HEAT_INDEX'], mta_df['CROWD_INDEX'],
            c=mta_df['RISK_INDEX'],
            cmap='Spectral_r', alpha=0.75)
plt.xlabel('HEAT INDEX')
plt.ylabel('CROWD INDEX')
plt.colorbar(label='RISK INDEX')

# save figure
plt.savefig(plot_path + '/new-york-station-heat_v_crowd.png', dpi=300)
plt.close()



print('\nCreating risk index station map...\n')
fig, ax = plt.subplots(2,1, figsize=(10,8), gridspec_kw={'height_ratios': [20,1]})

# plot risk index at each station, bluer colors are lower risk index
heat_df.plot(edgecolor='k',color='none',linewidth=0.1,
             ax=ax[0])
ax[0].scatter(mta_df['LON'], mta_df['LAT'], s=20, alpha=0.8, c=mta_df['RISK_INDEX'], cmap='Spectral_r')
ax[0].axis('off')
ax[0].set_title('Heat-Illness Risk Index', fontsize=24)

# create the custom colorbar and add labels
range_index = np.arange(1.0,10.0+0.01,0.01)

ax[1].scatter(range_index, np.ones(len(range_index)), c=range_index, cmap='Spectral_r', s=50, marker='|')
ax[1].axis('off')
ax[1].text(1.0,0.25,
             'risk index\n1',
             ha='center', fontsize=18)
ax[1].text(10.0,0.25,
             'risk index\n10',
             ha='center', fontsize=18)

# save figure
plt.savefig(plot_path + '/new-york-station-risk-index.png', dpi=300)
plt.close()

def nearby_low_risk(station, linename, risk_index, high_risk_lat, high_risk_lon):

    # create df of low risk stations
    linename_array = np.asarray(mta_df['LINENAME'])
    mask_low_risk = [True if len(set(l).intersection(linename)) != 0 else False for l in linename_array]
    low_risk = mta_df[(mta_df['RISK_INDEX'] <= 6) & mask_low_risk]

    if risk_index <= 6:
        return np.nan, np.nan, np.nan
    else:
        # calculate the distance from the high risk station to every low risk station
        distance_calc = np.array([distance.distance((high_risk_lat, high_risk_lon), (lat, lon)).miles for lat, lon in zip(low_risk['LAT'], low_risk['LON'])])
        # ignore stations that are too close (and likely also have high risk indices)
        mask = (distance_calc > 0.001) & (distance_calc < 0.75)
        distance_calc = distance_calc[mask]
        low_risk = low_risk[mask]
        if len(distance_calc) > 0:
            return low_risk['STATION'].iloc[np.argmin(distance_calc)], low_risk['LINENAME'].iloc[np.argmin(distance_calc)], np.min(distance_calc).round(3)
        else:
            return np.nan, np.nan, np.nan

mta_df[['NEAR_LOW_RISK_STATION','NEAR_LOW_RISK_LINENAME','NEAR_LOW_RISK_STATION_DIST']] = mta_df.apply(lambda x: nearby_low_risk(x['STATION'], x['LINENAME'], x['RISK_INDEX'], x['LAT'], x['LON']), axis=1, result_type='expand')

print(mta_df.sort_values('RISK_INDEX', ascending=False).head(15))


# save final combined dataframe
# if saved file already exisits, delete
if os.path.exists('heat_risk_index.csv'):
    os.remove('heat_risk_index.csv')

mta_df.to_csv('heat_risk_index.csv')
