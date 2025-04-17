# HURRICANE READINESS

Final Project for EECS 486: Information Retrieval

This project aims to help legistlators and activists to estimate property damage homeowners may face living in their county. 

The repository offers the following options:

- Compare our predictive Feed Forward Neural Net (FFNN) model compares to actual historic data 

<video width="640" height="360" controls>
  <source src="assets/video_demo/Search_Existing_Results.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

- Manually enter your own county's data to see an estimate of property damage per person your county can expect this upcoming year 

<video width="640" height="360" controls>
  <source src="assets/video_demo/Manual_Entry.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

- Prompt an LLM with the relevant context about your area so it can make a predictition about information about your county (such as Population, Dam count, Hurricane Freq, etc.) to use as an input for the FFNN.

<video width="640" height="360" controls>
  <source src="assets/video_demo/Chatbot_Assisted_Prediction.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

- See our methodology

<video width="640" height="360" controls>
  <source src="assets/video_demo/Methodology.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


****WARNING** in these videos we used gpt-4o-mini, however the instructions below use llama3.2:latest. This discrepancy impacts time for the Manual Entries & Chatbot Assisted Prediction substatially. Read the messages printed from the terminal running `api/page.py` to make sure it is loading correctly.

## Repo Structure

<pre>
.
├── README.md
├── api                                       // Run to call NN and LLMs
│   └── page.py
├── assets                                    // Various Assets for the UI/video tutorials
│   ├── fema_regions_map.png
│   ├── heatmap_images
│   └── video_demo
├── collect_data                             // Scripts to format all data to JSON
│   ├── Dams
│   ├── FEMA-DDS
│   └── FEMA-HRI
├── evaluation                               // Scripts to evaluate performance
│   └── performance.py
├── list.txt
├── metrics.txt
├── predicted_list.txt
├── predictive_model                         // Information about the Feed Forward Neural Net AND other attempted models
│   ├── logistic_nb_model.py
│   ├── model.pth
│   ├── multiple_linear_regression.py
│   ├── neural_network.py
│   └── scaler.pkl
├── processed_data                           // Scripts to combine all JSON files above into one usable CSV file
│   ├── data.csv
│   ├── heatmap_slider.py
│   ├── load_data.py
│   └── preprocess.py
├── raw_data                                 // Initialled downloaded files from websites listed below
│   ├── Dams
│   ├── FEMA-DDS
│   ├── FEMA-HRI
│   └── cb_2022_us_county_5m
├── requirements.txt                         // Python libraries
└── website                                  // UI to interface with the data
    ├── index.html
    └── style.css
</pre>

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

### Change LLM (Optional)

Default LLM is llama3.2:latest as explained above but this project also supports deepseek-r1:8b and gpt-4o-mini

#### Deepseek-r1
1.) Run `ollama run deepseek-r1:8b` in terminal with ollama
2.) Type `\bye` when installed
3.) In `api/page.py` change the variable named llm to `"deepseek"`.

#### gpt-4o-mini
1.) Go to [OpenAI API](https://openai.com/api/) and follow instructions to make an API key
2.) Create a file named `.env` in the root directory of this repo
3.) In `.env` write the `OPENAI_API_KEY=<your api key>` 
3.) In `api/page.py` change the variable named llm to `"chatgpt"`.

## Collect Data:

This is only for those wanting more up-to-date data than 4/15/2025. 

**Not all files required to update the dataset are included in this repo.**

They are not included as Github prevents large files to be stored in repos.

If interested, these datasets can be found at the following:
- [FEMA Natural Disaster Log](https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2)
- [FEMA Hurricane Data](https://hazards.fema.gov/nri/hurricane)
- [National Inventory of Dams](https://nid.sec.usace.army.mil/#/dams/search/&viewType=map&resultsType=dams&advanced=false&hideList=false&eventSystem=false)

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