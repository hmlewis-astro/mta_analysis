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


#### Aggregation

#### Visualization


### Tools
- SQLAlchemy for querying SQL database in Python
- Mapshapper (employed by pre-packaged analysis algorithms by the USGS) for creating and altering geographic databases
- Pandas, GeoPandas, and Numpy for data analysis
- GeoPandas for handling and plotting geographic data
- Matplotlib for plotting
- Tableau for interactive visualizations

### Communication

In addition to the slides and visuals presented here, the Tableau dashboard [NYC MTA Heat](https://public.tableau.com/views/NYCMTAHeatAnalysis/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link) will be included in a forthcoming blog post to be shared on my (work-in-progress) GitHub Pages [website](https://hmlewis-astro.github.io/).
