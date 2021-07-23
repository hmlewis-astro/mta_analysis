# Project Write-Up
## Avoiding heat-illness in New York City's busiest and hottest MTA stations


### Abstract

The goal of this project was to (1) determine the MTA stations that pose the greatest hazard&mdash;due to the combination of high heat and large crowds&mdash;to people at high-risk for heat-related illnesses, and to (2) the general public with access to this information, so that people a high-risk for heat-illness (e.g., adults over the age of 65, people with existing health conditions) can make more informed decisions about which MTA stations to avoid to maintain their personal health. I compared [subway turnstile data](http://web.mta.info/developers/turnstile.html) provided by the MTA with corresponding surface temperature data collected by the [NASA Landsat 8 satellite](https://landsat.gsfc.nasa.gov/landsat-8/landsat-8-overview) to create a heat-illness risk index for subway stations in the MTA system. After determining the highest heat-illness risk stations, I built an interactive Tableau dashboard to visualize and publicize these results.


### Design

This project comes at the request of the New York City Department of Health; for an upcoming press release concerning summer heat, the Department wants to compile a list of MTA stations that pose the greatest risk to people at high-risk for heat-related illnesses. Because heat stress and heat-related illnesses are exacerbated by conditions that are incredibly crowded (in addition to extremely hot), they want to understand which stations are most impacted by _both of these factors_ (i.e., heat and crowds). By providing daily subway users with this information, the Department hopes to prevent a spike in heat-related illnesses this summer, and allow MTA riders to make informed decisions regarding their subway use during future heat waves.

### Data

#### Heat data
Satellite imagery of New York City (with <1% cloud cover) was captured during Summer 2018 by the NASA Landsat 8 satellite. This image, downloaded from [Earth Explorer](https://earthexplorer.usgs.gov/), captured a roughly 185 km by 180 km (114 mi by 112 mi) image of the land area in 11 spectral bands (file size ~70 MB); for each image pixel, brightness measurements in multiple bands can be combined (via known relations; see Algorithms section below) to derive precise land temperature measurements. Surface temperatures can be estimated with 30 meter spatial resolution.

#### Crowd-size data
The MTA publishes weekly turnstile data that provides transit ridership as measured by turnstile entries and exits, with readings taken approximately every 4 hours. Though data is available going back to 2010, the database utilized here contains ridership data only for the year of 2018 (to correspond with the captured satellite imagery; ~10.3M rows, file size ~800 MB). Geolocations (i.e., latitude, longitude coordinates) for most MTA stations are collected from a publicly available [datafile](https://github.com/chriswhong/nycturnstiles/blob/master/geocoded.csv), though some stations were added by-hand to the [file available in this repo](https://github.com/hmlewis-astro/mta_analysis/blob/main/geocoded.csv).


### Algorithms

#### Cleaning & EDA
Given the NASA Landsat 8 image, the New York City Census block shapefile is used as reference to extract spectral radiances, and derive the median temperature within each Census block; outliers are replaced with the 1st and 99th percentile temperature values. From the observed temperature variations over the land area, a "heat index" in the range of 1 to 10 is calculated and assigned to each Census block, 10 being a land area with higher than median heat, 1 with lower than median heat.

Given the SQL database containing MTA turnstile data, I create a new table within that database with the available geolocation information. Using SQLAlchemy in Python, these tables are joined (on the `booth`/`C/A` and `unit`) so that each turnstile now also has an associated latitude and longitude. In this query, I also create a new `system` key which differentiates stations in the MTA versus PATH systems. From the database containing all turnstile data for the year 2018, only data collected during summer months (i.e., between 06/01/2018 and 08/31/2018) were selected for this analysis.

I then calculate the time passed (in seconds) and the change in the turnstile `entries` counts between each reading; again, readings occur roughly every four hours. Here, there are two peculiarities in the data: (1) some turnstiles are counting backwards and (2) turnstiles appear to reset, leading to apparent increases in `entries` on the order of 10<sup>5</sup>-10<sup>7</sup> riders over just a few hours. To deal with these, I (1) always take the absolute value of the number of entries between measurements and (2) set an upper limit of 3 entries per turnstile per second. The later of these allows for a dynamic upper-limit to be set for each observation, depending on the time between measurements, rather than setting a single upper-limit.

#### Aggregation
The cleaned MTA data are then aggregated by station and linename, such that the net entries over the observed three month period can be derived. From the net entries, a "crowd index" in the range of 1 to 10 is calculated for each station, 10 being the most crowded, 1 being the least.

The MTA and heat data are then joined together based on the spatial location of each station.

By combining the derived "heat index" and "crowd index" for each station, I calculate a "risk index" (again, scaled from 1 to 10, with 10 being high risk) for heat-illness at each station.

#### Visualization
Maps of the stations colored by the various indices presented here are created.

Example: A map of New York City's subway stations, where each station location is colored by its "risk index", which considers heat-illness risk due to both high heat and large crowds. Redder colors indicate higher-risk stations.

<p align="center">
<img src="https://github.com/hmlewis-astro/mta_analysis/blob/main/heat_data/data/output/analysis_out/final/plots/new-york-station-risk-index.png" width="512" />
</p>


### Tools
- SQLAlchemy for querying SQL database in Python
- Mapshapper (employed by pre-packaged analysis algorithms by the USGS) for creating and altering geographic databases
- Pandas, GeoPandas, and Numpy for data analysis
- GeoPandas for handling and plotting geographic data
- Matplotlib and Tableau for plotting and interactive visualizations

### Communication

In addition to the slides and visuals presented here, the Tableau dashboard [NYC MTA Heat](https://public.tableau.com/views/NYCMTAHeatAnalysis/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link) will be included in a forthcoming blog post to be shared on my (work-in-progress) GitHub Pages [website](https://hmlewis-astro.github.io/).

<p align="center">
<img src="https://github.com/hmlewis-astro/mta_analysis/blob/main/final_pres/NYC_MTA_heat_dashboard.png" width="512" />
</p>
