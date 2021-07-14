# Project Proposal
<h2>Extremely Hot and Incredibly Crowded:</h2>
<h3>avoiding heat-illness in New York City's busiest MTA stations</h3>

Heat stress and heat-related illnesses occur when the body is unable to cool itself and maintain a healthy temperature, and begins to overheat. Heat illness symptoms can range from mild (e.g., a rash or muscle spasms) to severe (e.g., heatstroke), and can kill.

Although anyone can suffer from heat-related illness, adults over the age of 65, infants and young children, and people with existing health conditions (such asthma, COPD, heart disease, or high blood pressure) are at greater risk than others.

Heat stress can be exacerbated by conditions that are excessively hot and extremely crowded.

### Question:

For an upcoming press release concerning summer heat, the New York City Department of Health and Mental Illness wants to compile a list of MTA stations that pose the greatest hazard&mdash;due to the combination of high heat and large crowds&mdash;to people at high-risk for heat-related illnesses. Given such information, people in high-risk groups can then make more informed decisions about which MTA stations they might opt to avoid to maintain their personal health.

### Data description:

The [urban heat island effect](https://scied.ucar.edu/learning-zone/climate-change-impacts/urban-heat-islands)&mdash;that cities tend to be hotter than their natural surroundings&mdash;is a well studied phenomenon; however, it has also been shown that *within* cities temperatures vary by up to 10s of degrees due to variation in tree cover and impervious ground (i.e., pavement/blacktop) cover (see e.g., [this article by NPR](https://www.npr.org/2019/09/03/754044732/as-rising-heat-bakes-u-s-cities-the-poor-often-feel-it-most)).

To determine those MTA stations that pose the greatest risk due to extreme heat, we will utilize thermal imagery of New York City captured during summer months (defined as June, July, or August) from the NASA Landsat 8 satellite. Satellite images are openly available for download from [EarthExplorer](https://earthexplorer.usgs.gov/) and (on average) all land area is imaged one time per month. Images are collected regardless of cloud cover or weather conditions. Though a given land area may be imaged monthly, a number of those images may have a large area of land obscured by clouds; this prevents the extraction of precise thermal measurements.

We will select the most recently available image (avoiding the summers of 2020 and 2021, when MTA traffic was significantly impacted by the COVID-19 pandemic) with low cloud cover over the entire area of New York City that was collected during a summer month. From this image, surface temperatures at the latitude and longitude of each MTA station can be extracted (with 30 meter spatial resolution); stations can then be ranked by a relative heat index.

The New York MTA publishes weekly turnstile data that provides ridership as measured by turnstile entries and exits, with readings taken every 4 hours, and [data publicly available](http://web.mta.info/developers/turnstile.html) going back to 2010. Based on available high-quality NASA Landsat satellite imagery captured during summer months (June, July, or August) in a given year, we will collect the weekly MTA transit data for that year's summer months. That is, if a quality satellite imagery are available


### Tools:


### MVP:
