# Minimum Viable Product
## Extremely Hot and Incredibly Crowded: avoiding heat-illness in New York City's busiest MTA stations

The goal of this project is to determine the MTA stations that pose the greatest hazard&mdash;due to the combination of high heat and large crowds&mdash;to people who are at high-risk for heat-related illnesses.

To determine the MTA stations posing the greatest risk due to **extreme heat**, we utilize thermal imagery of New York City captured during summer months (defined as June, July, or August) from the NASA Landsat 8 satellite. The temperature in each Census block (from NYC OpenData) is derived from an image captured during Summer 2018, and a heat index from 1 (low heat, low-risk) to 10 (high heat, high-risk) is assigned to each block. The map below shows the heat index over the entire city; blue/green colors represent land areas with low heat indices (generally, near water or green-space), and orange/red colors represent areas with high heat indices (denser cityscapes or airports).

<p align="center">
<img src="https://github.com/hmlewis-astro/mta_analysis/blob/main/heat_data/data/output/analysis_out/final/plots/new-york-heat-index.png" width="800" />
</p>


To determine the MTA stations that pose a risk due to **crowds**, we use the total number of turnstile entrances at each station (over June, July, August 2018) to determine the relative number of riders at each station. A crowd index from 1 (small crowds, low-risk) to 10 (large crowds, high-risk) is assigned to each station based on the total number of riders during the analyzed months. The map below shows the crowd index for each station; blue/green colors represent stations with smaller crowds, and orange/red colors represent stations with larger crowds.

<p align="center">
<img src="https://github.com/hmlewis-astro/mta_analysis/blob/main/heat_data/data/output/analysis_out/final/plots/new-york-crowd-index.png" width="800" />
</p>


These results show that there is a significant variation in *both* temperature and MTA ridership over the entire city. Understanding separately the impact of heat and crowds on each station is an important step in reaching our ultimate goal of creating a heat-illness risk index (which accounts for risk due to both heat and crowding) for each station.

To create a heat-illness risk index, the datasets containing the Census block heat indices and the station crowd indices need to be merged based on the Census block within which each station is located. Using the known geometry for each Census block, and the latitude and longitude coordinates for each station, we will assign each station a heat index from the heat index map.
