# Minimum Viable Product
## Extremely Hot and Incredibly Crowded: avoiding heat-illness in New York City's busiest MTA stations

The goal of this project is to determine which MTA stations pose the greatest hazard&mdash;due to the combination of high heat and large crowds&mdash;to people at high-risk for heat-related illnesses.

<img src="https://github.com/hmlewis-astro/mta_analysis/blob/main/heat_data/data/output/analysis_out/final/plots/new-york-heat-index.png" width="1024" />


![crowd index map](https://github.com/hmlewis-astro/mta_analysis/blob/main/heat_data/data/output/analysis_out/final/plots/new-york-crowd-index.png)

### Data description:

#### Heat data
The [urban heat island effect](https://scied.ucar.edu/learning-zone/climate-change-impacts/urban-heat-islands)&mdash;that cities tend to be hotter than their natural surroundings&mdash;is a well studied phenomenon; however, it has also been shown that *within* cities temperatures vary by up to 10s of degrees due to variation in tree cover and impervious ground (i.e., pavement/blacktop) cover (see e.g., [this article by NPR](https://www.npr.org/2019/09/03/754044732/as-rising-heat-bakes-u-s-cities-the-poor-often-feel-it-most)).

To determine those MTA stations that pose the greatest risk due to extreme heat, we will utilize thermal imagery of New York City captured during summer months (defined as June, July, or August) from the NASA Landsat 8 satellite. Satellite images are openly available for download from [EarthExplorer](https://earthexplorer.usgs.gov/) and (on average) all land area is imaged one time per month. Images are collected regardless of cloud cover or weather conditions, so though a given land area may be imaged monthly, a number of those images may have a large area of land obscured by clouds; this prevents the extraction of precise thermal measurements.

We will select the most recently available image (avoiding the summers of 2020 and 2021, when MTA traffic was significantly impacted by the COVID-19 pandemic) with low cloud cover (<10% coverage) over the entire area of New York City that was collected during a summer month. From this image, surface temperatures at the latitude and longitude of each MTA station ([available here](http://web.mta.info/developers/developer-data-terms.html#data)) can be extracted with 30 meter spatial resolution; stations can then be ranked by a relative heat index.

#### Crowd-size data
The MTA publishes weekly turnstile data that provides ridership as measured by turnstile entries and exits, with readings taken every 4 hours, and [data publicly available](http://web.mta.info/developers/turnstile.html) going back to 2010. Based on the year of the selected high-quality NASA Landsat satellite image (see above for selection criteria), we will collect the weekly MTA transit data for the summer months of that year. That is, if a quality satellite image of New York City is available in June 2018, we will collect the weekly MTA transit data for all weeks spanning June through August 2018. We will use the total number of turnstile entrances/exits at each station to determine the relative number of riders at each station compared to the total number of MTA users, and use this value as a proxy for a crowding index.
<!--This calculation will assume that all stations are the same size (i.e., area in square feet), which may be a flawed assumption.-->

By combining the heat and the crowding indices into a risk index, we will be able to determine which MTA stations pose the greatest hazard to people at high-risk for heat-related illnesses.

### Tools:

To download the MTA turnstile data and create an SQL database, we will use the python script `get_mta.py`, [available here](get_mta.py). To query from that database into Python, we will use SQLAlchemy, and from that query, we will create a pandas dataframe with the MTA turnstile data  and corresponding latitude, longitude coordinates for each station.

We will use [previously developed algorithms](https://www.usgs.gov/core-science-systems/nli/landsat/landsat-collection-2-surface-temperature) from the US Geological Survey to extract surface temperature measurements from the selected NASA Landsat 8 satellite image. These algorithms create a `.geojson` file with surface temperature measurements, and the corresponding latitude and longitude coordinates at each measurement, over the image area. This file will be read into Python with the geopandas package, and can be merged with the pandas dataframe containing the MTA turnstile data.

We will use the pandas and matplotlib packages to explore that data, derive the heat and crowding indices, determine the risk index for each MTA station (by some weighted combination of the heat and crowding indices), and produce a list of the highest risk MTA stations for heat illnesses. Given sufficient time, we may also utilize the plotly package to present the risk index for each station on an interactive map.


### MVP:

The minimal viable product (MVP) for this project will likely be the calculation of the heat and crowding indices (separately) for each MTA station. To completely address the needs of the New York City Department of Health for their press release, we need to combine these two metrics into a single risk index and present these results in a way that can be easily consumed by the general public; however, understanding separately the impact of heat and crowds on each station is an important step in reaching this ultimate goal.
