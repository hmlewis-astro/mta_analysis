#!/usr/bin/env python
# coding: utf-8


import os

# if MTA database already exisits, delete to avoid duplicating data
#if os.path.exists('mta_data.db'):
    #os.remove('mta_data.db')

# get MTA data from same year as satellite image
#os.system('python get_mta.py "18"')



# import SQLAlchemy
from sqlalchemy import create_engine, inspect

# import data analysis, plotting packages
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



def insert_table_from_csv(csv_list, engine):
    """
    Adds a .csv as a table in an SQL database
    """
    for file in csv_list:
        with open(file, 'r') as f:
            data = pd.read_csv(f)
            data.columns = data.columns.str.strip()
        data.to_sql(os.path.splitext(file)[0], con=engine,
                    index=False, if_exists='replace')



# create SQL database engine
mta_data_engine = create_engine("sqlite:///mta_data.db")

# add the geocoded station locations as a table in the MTA database
insert_table_from_csv(['geocoded.csv'], mta_data_engine)

# make sure that the geocoded table was added
insp = inspect(mta_data_engine)
print('\nTables in database:', insp.get_table_names(), '\n')

# rename column 'C/A' in the mta_data table to 'BOOTH' for consistency with the
# geocoded table
#pd.read_sql('''
            #ALTER TABLE mta_data
            #RENAME COLUMN "C/A" TO "BOOTH";
            #''',
            #mta_data_engine);

# join mta_data and geocoded tables on the booth and unit numbers
# select turnstile-level information, include entries and exits, date, time,
# latitude, longitude
# add 'SYSTEM' to differentiate turstiles in the PATH vs. MTA systems
# -- note: many PATH systems are missing lat/lon coordinates, so will likely
#    need to drop them later
# keep only summer (June, July, August) data and 'REGULAR' scheduled audit
# events, not 'RECOVR AUD' entries to avoid duplicates
mta_df_read = pd.read_sql('''
            SELECT a.booth, a.unit, a.scp, a.station, a.linename, a.division,
              a.date, a.time,
              (a.date || ' ' || a.time) AS DATE_TIME,
              a.entries, a.exits,
              b.lat AS LAT, b.lon AS LON,
              (CASE
                WHEN b.booth LIKE '%PTH%' THEN 'PATH'
                ELSE 'MTA'
              END) AS SYSTEM
            FROM mta_data a
            LEFT JOIN geocoded b
            ON a.booth = b.booth AND a.unit = b.unit
            WHERE a.date >= '06/01/2018'
              AND a.date <= '08/31/2018'
              AND a.desc = 'REGULAR';
            ''',
            mta_data_engine)

mta_df = mta_df_read.copy(deep=True)



# convert 'DATE_TIME' column to datetime format
mta_df['DATE_TIME'] = pd.to_datetime(mta_df.DATE_TIME,
                                     format = '%m/%d/%Y %H:%M:%S')

# sort linenames
mta_df['LINENAME'] = mta_df['LINENAME'].apply(lambda x: ''.join(sorted(x)))

mta_df.sort_values('DATE_TIME', ascending=True, inplace=True)



# new columns with the datetime of the previous measurement, and entries
# measurement at the previous measurement
mta_df[['PREV_DATE_TIME', 'PREV_ENTRIES']] = mta_df.groupby(['BOOTH', 'UNIT', 'SCP', 'STATION'])[['DATE_TIME', 'ENTRIES']].shift(1)

# drop the rows for the first measurement in the df because there is no
# 'PREV_DATE_TIME', and reset the index
mta_df.dropna(subset=['PREV_DATE_TIME'], axis=0, inplace=True)
mta_df.reset_index(drop=True, inplace=True)



# calculate the amount of time (in seconds) between measurements
mta_df['DELTA_DATE_TIME_SEC'] = np.abs(mta_df['DATE_TIME'] - mta_df['PREV_DATE_TIME']) / pd.Timedelta(seconds=1)

# to deal with turnstiles that are counting in reverse, always take the abs
# value of the difference between current entries and previous entries
# for hourly entries that are very high, as an upper limit, use 3 people per
# turnstile per second
pps = 3
mta_df['HOURLY_ENTRIES'] = [np.abs(entries - mta_df['PREV_ENTRIES'][i]) \
                            if (np.abs(entries - mta_df['PREV_ENTRIES'][i]) < pps*mta_df['DELTA_DATE_TIME_SEC'][i]) \
                            else (pps*mta_df['DELTA_DATE_TIME_SEC'][i]) \
                            for i,entries in enumerate(mta_df['ENTRIES'])]



# group unique stations (some stations have the same name, but are on different
# lines)
# sum the hourly entries to get the total number of entries over the time period
# sort by net entries
station_df = mta_df.groupby(['STATION','LINENAME'], as_index=False).agg({'LAT':'first', 'LON':'first', 'SYSTEM':'first', 'HOURLY_ENTRIES':'sum'}).sort_values('HOURLY_ENTRIES', ascending=False)

# check which stations still don't have lat/lon coordinates
#print(station_df[np.isnan(station_df['LAT'])])

# rename the 'HOURLY_ENTRIES' column to 'NET_ENTRIES'
station_df.rename(columns={'HOURLY_ENTRIES': 'NET_ENTRIES'}, inplace=True)

# reset index so that index corresponds to ranked net entries
station_df.reset_index(drop=True, inplace=True)

# drop the few stations that still don't have lat/lon coordinates
station_df.dropna(inplace=True)



# create 'CROWD_INDEX'
min_entries = np.min(station_df['NET_ENTRIES'])
max_entries = np.max(station_df['NET_ENTRIES'])
# scale the log of the net entries of each station from 1 to 10 (10 being the most crowded, 1 being the least)
station_df['CROWD_INDEX'] = station_df['NET_ENTRIES'].apply(lambda x: 1.0 + 9.0 * np.log10(x/min_entries) / np.log10(max_entries/min_entries))


# pickle final dataframe
# if pickled file already exisits, delete
if os.path.exists('mta_data_analyzed.csv'):
    os.remove('mta_data_analyzed.csv')

station_df.to_csv('mta_data_analyzed.csv')
