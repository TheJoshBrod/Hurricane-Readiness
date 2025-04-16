# HURRICANE READINESS

Final Project for EECS 486: Information Retrieval

In this project we present a method of both viewing existing and predicting new property damage due to hurricanes. 

This repo offers a UI to interact with the data collected and models created to offer:
- Search Existing State: Comparisons of historical property damage/person for all counties




- Manually Predict a New County: 


## SET-UP PROJECT 

This repo already includes all of the csv/json/photos needed for the project to run, you just need to install/run the following commands

### General Python Set-Up

1.) Install [Python3.X](https://www.python.org/downloads/)

2.) Run the following `pip install -r requirements.txt`

### General Ollama/llama3.2 Set-Up

1.) Install [Ollama](https://ollama.com/download/linux), follow instruction on the page

2.) Once installed run `ollama serve` in a terminal of the OS Ollama was installed for (Windows: powershell, WSL: ubuntu, etc.)

3.) When Ollama serve is running, in a new terminal run `ollama run llama3.2:latest`

4.) Wait until the model finishes installing, then close that terminal with `/bye` (leave the other terminal where you ran `ollama serve` running)

### Start the backend API

1.) run `python3 api/page.py`

### Open the front-end UI

1.) Open the `website/index.html` file with your browser, this can be done by opening your file explorer and double clicking on the `website/index.html` file

## Simple walk through of using program:



## Update Collection of Data:

This is only for those wanting more up-to-date data than 4/15/2025

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