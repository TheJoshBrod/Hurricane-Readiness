# HURRICANE READINESS

Final Project for EECS 486: Information Retrieval

## ABOUT

As climate change brings more frequent and more unpredictable storms, people are often faced with devastation to personal property, and emotional anguish over losing possessions that have been with their families for generations. Hurricanes, in particular, have both increased in intensity and unpredictability. As future generations are faced with these increasingly dangerous storms, we want to make sure that people are more prepared and ready to weather the natural disasters ahead.

Hurricanes are especially hard-hitting due to both torrential rainfall and wind speeds that can decimate infrastructure. In the past decade, storms that caused high casualties and unprecedented property damage have one thing in common: failure of the dam system. During Hurricane Katrina in 2005, the levees around the city failed. This flooded about 80\% of the city for weeks, stranding survivors. In addition, stagnant water spread black mold to millions of homes, making them uninhabitable after the storm. During hurricane Harvey, in 2017, the dams were breached, letting unprecedented flooding into residential areas, impacting the homes of millions once again. Just last year, the failure of the Lake Lure dam in North Carolina caused even more damage and loss of life. All of these dams were classified as high risk; if they broke, people would die. And yet, all of them weren’t maintained or updated, leaving these areas vulnerable to disaster. However, what made the North Carolina disasters so dangerous was climate change. Previously, inland North Carolina had received residual rainfall from hurricanes, like remaining rain bands and more. However, last year, the hurricane traveled further inland than ever before, bringing flooding and damage unlike anything the region had seen. Dam inventory can help, but only if one knows where to look.
	
Our project is to try and raise awareness to these high risk dams, and make sure any disrepair is remedied before it's too late. By using the national inventory of dams, we are going to find a ranked list of both highest risk and least maintained dams in hurricane regions, finding the areas at most critical danger. However, as weather patterns change, so do the areas where hurricanes make landfall and impact. Because of this, we are also going to try and predict the newer hurricane prone area, and take this into account. If an area is newly hurricane prone and has unmaintained high-risk dams, those areas are more critical than those currently in hurricane zones due to their lack of familiarity and preparation on the subject. So, taking into account historical hurricane data, new weather patterns, dam risk, and dam maintenance, we hope to find the areas most unprepared for such a natural disaster and raise awareness so they can save their community before climate change strikes.

According to NASA, "There are 4 key elements needed for a hurricane: warm ocean water, lots of moisture in the air, low vertical wind shear, and a pre-existing disturbance (e.g., a cluster of thunderstorms)"\cite{NASA}. As climate change starts to increase temperatures across the globe, its important to consider which areas now posses all these factors, when they didn't previously. With rising sea levels, more areas are closer than ever to warm ocean water, so checking who is in proximity now can help estimate where we need to consider. Also, as the world warms up, there's more available moisture in the air, bringing two of the most critical and hardest factors of hurricanes to more regions than ever before. By trying to figure out where these areas are, we can then cross reference our list of dams that aren't maintained or are at risk of breaching with these newly endangered regions, and hopefully warn residents before they get hit with the next wave of storms.

## SET-UP PROJECT

### General Python Set-Up

1.) Install [Python3.X](https://www.python.org/downloads/)

2.) Run the following `pip install -r requirements.txt`

### Data Collection Set-Up

Start by attempting to automatically download the necessary data. If you have issues downloading it automatically, go through the steps to download it manually.

#### Automatically Download Data

To automatically download all data, execute:
```bash
python3 processed_data/load_data.py
```
If this is successful, proceed to "Processing Data" and skip all manual downloads.

#### Manually Download Data: Disaster Declaration Summaries

- Download [FEMA Disaster Declarations Summaries](https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2) and save it as:  
  `raw_data/FEMA-DDS/all_disasters.json`

- Run the following command to format and filter the raw data:  
  ```bash
  python3 collect_data/FEMA-DDS/FilterDDS.py
  ```
    * Formats raw_data and filters data to only relevant disasters 

- When attempting to update your dataset run  
  ```bash
  python3 collect_data/FEMA-DDS/UpdateDDS.py
  ```

#### Manually Download Data: FEMA-HRI

- Download [FEMA Hurricane Risk Index](https://hazards.fema.gov/nri/data-resources#csvDownload), clicking `All Counties - County-level detail (Table)`

- Unzip the file and take out `NRI_Table_Counties.csv` and save it as:  
  `raw_data/FEMA-HRI/all_counties.csv`

- Run the following command to format and filter the raw data:  
  ```bash
  python3 collect_data/FEMA-HRI/FilterHRI.py
  ```
    * Formats raw_data and filters data to only relevant disasters 

#### Manually Download Data: Dam Data Processing

This component processes dam data from the National Inventory of Dams. **Note:** The dataset (`nation.csv`) and the resulting output JSON file (`dam_data.json`) are very large and are not included in this repository.

##### Setup

- Download the National Inventory of Dams CSV file and save it as `nation.csv` in the project root directory.

##### Running the Dam Data Code

The dam data processing is managed by the `dams.py` script.

To run the dam data processing, execute:
```bash
python3 dams.py
```

### Processing Data

To process the data, execute:
```bash
python3 processed_data/preprocess.py
```

### Visualizing Data

- Run `python3 api/page.py`
    - This will start the api that will retrieve all of our data

- Open `website/index.html`
