#!/usr/bin/env python
# coding: utf-8

# get MTA data from same summer as satellite image
import os
import time

os.system('python get_mta.py "17"')
time.sleep(60)

import sqlite3 as sq
from sqlalchemy import create_engine, inspect, Table, MetaData
from sqlalchemy.orm import sessionmaker

import pandas as pd

mta_data_engine = create_engine("sqlite:///mta_data.db")

def insert_table_from_csv(csv_list, engine):
    for file in csv_list:
        with open(file, 'r') as f:
            data = pd.read_csv(f)
            data.columns = data.columns.str.strip()
        data.to_sql(os.path.splitext(file)[0], con=mta_data_engine, index=False, if_exists='replace')

insert_table_from_csv(['mta_stations_loc.csv', 'mta_complex_id.csv'], mta_data_engine)

insp = inspect(mta_data_engine)
print(insp.get_table_names())

pd.read_sql('''
            ALTER TABLE mta_data
            RENAME COLUMN "C/A" TO "BOOTH";
            ''',
            mta_data_engine)

temp_df = pd.read_sql('''
            SELECT a.booth, a.unit, a.scp, a.station, a.linename, a.division,
              MAX(a.entries)-MIN(a.entries) AS net_entries,
              MAX(a.exits)-MIN(a.exits) AS net_exits,
              CAST(b.complex_id AS int) AS complex_id,
              c."GTFS Latitude" AS lat, c."GTFS Longitude" AS lon
            FROM mta_data a
            JOIN mta_complex_id b
            JOIN mta_stations_loc c
            ON a.booth = b.booth AND a.unit = b.remote AND b.complex_ID = c."Complex ID"
            WHERE a.date >= '06/01/2017'
              AND a.date <= '08/31/2017'
              AND a.desc = 'REGULAR'
            GROUP BY a.booth, a.unit, a.scp;
            ''',
            mta_data_engine)

mta_df = pd.read_sql('''
            SELECT booth, unit, station, linename, division, SUM(net_entries)+SUM(net_exits) AS net_rides, complex_id, lat, lon
            FROM
            (SELECT a.booth, a.unit, a.scp, a.station, a.linename, a.division,
              MAX(a.entries)-MIN(a.entries) AS net_entries,
              MAX(a.exits)-MIN(a.exits) AS net_exits,
              CAST(b.complex_id AS int) AS complex_id,
              c."GTFS Latitude" AS lat, c."GTFS Longitude" AS lon
            FROM mta_data a
            JOIN mta_complex_id b
            JOIN mta_stations_loc c
            ON a.booth = b.booth AND a.unit = b.remote AND b.complex_ID = c."Complex ID"
            WHERE a.date >= '06/01/2017'
              AND a.date <= '08/31/2017'
              AND a.desc = 'REGULAR'
            GROUP BY a.booth, a.unit, a.scp)
            GROUP BY complex_id;
            ''',
            mta_data_engine)

mta_df

import geopandas as gpd
print('imported geopandas')
