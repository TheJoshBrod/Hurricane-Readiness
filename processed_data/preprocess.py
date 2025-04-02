import os
import shutil
import requests
import zipfile
import json
import io
from datetime import timedelta, datetime
import pandas as pd

import matplotlib.pyplot as plt


import warnings
warnings.simplefilter("ignore", DeprecationWarning)


def load_dams_data(original: pd.DataFrame):
    # read nation.csv
    df = pd.read_csv("raw_data/Dams/nation.csv", skiprows=1)

    # get hazard score for each dam
    hazard_score = {
        "Undetermined": 1,
        "Low": 3,
        "Significant": 5,
        "High": 10
    }
    df["Hazard Score"] = df["Hazard Potential Classification"].map(hazard_score)
    
    # aggregate average hazard score and number of dams
    df = df.groupby(['State', 'County'])['Hazard Score'].agg(['mean', 'count']).reset_index()
    
    # merge with original
    return pd.merge(original, df, left_on=['STATE', 'COUNTY'], right_on=['State', 'County'], how='inner').drop(columns=['State', 'County'])


def load_disasters_over_time(df: pd.DataFrame):
    """Get disaster frequency"""


    # Get all previously filtered disaster data
    data = {}
    with open("raw_data/FEMA-DDS/filtered_disasters.json") as f:
        data = json.load(f)["DisasterDeclarationSummaries"]
    new_df = pd.DataFrame.from_dict(data, orient='columns')
    
    # Convert all dates to date object
    new_df["disasterCloseoutDate"] = pd.to_datetime(new_df['disasterCloseoutDate'], format='%Y-%m-%dT%H:%M:%S.%fZ')

    # Get date object of each time stamp
    twenty_years_ago = datetime.utcnow() - timedelta(days=20*365)
    ten_years_ago = datetime.utcnow() - timedelta(days=10*365)
    five_years_ago = datetime.utcnow() - timedelta(days=365)
    one_years_ago = datetime.utcnow() - timedelta(days=365)

    # Filter for disasters happening x years ago
    disaster_counts = new_df.groupby(["fipsStateCode","fipsCountyCode"]).agg(
        DISASTER_PER_YEAR_20=("disasterCloseoutDate", lambda x: (x > twenty_years_ago).sum() / 20),
        DISASTER_PER_YEAR_10=("disasterCloseoutDate", lambda x: (x > ten_years_ago).sum() / 10),
        DISASTER_PER_YEAR_5=("disasterCloseoutDate", lambda x: (x > five_years_ago).sum() / 5),
        DISASTER_PER_YEAR_1=("disasterCloseoutDate", lambda x: (x > one_years_ago).sum()),
       
    ).reset_index()

    # Rename columns for consistency with df
    disaster_counts = disaster_counts.rename(columns={"fipsStateCode": "STATEFIPS", "fipsCountyCode": "COUNTYFIPS"})
    
    # Change typing of fips codes to be str
    df["STATEFIPS"] = df["STATEFIPS"].astype(str).str.zfill(2)
    df["COUNTYFIPS"] = df["COUNTYFIPS"].astype(str).str.zfill(3)

    # Merge DataFrames
    merged_df = pd.merge(df, disaster_counts, on=["STATEFIPS", "COUNTYFIPS"], how="left")
    merged_df.fillna(0, inplace=True)
    
    # Handle no hurricane areas
    count_zero_disasters_20 = (merged_df["DISASTER_PER_YEAR_20"] == 0).sum()
    merged_df = merged_df[merged_df["DISASTER_PER_YEAR_20"] != 0]
    
    return merged_df

def load_predicitve_data():
    """Load labels and input data for predictive model training."""
    folder_path = 'NRI_Data'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    url = 'https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_Table_Counties/NRI_Table_Counties.zip'
    response = requests.get(url)
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall('NRI_Data')  # Extracts to a directory named 'NRI_Data'

    # Read the CSV file from the URL
    df = pd.read_csv('NRI_Data/NRI_Table_Counties.csv', usecols=['COUNTY', 'COUNTYFIPS', 'STATEFIPS', 'STATE', 'STATEABBRV', 
                                                                 'POPULATION', 
                                                                 'HRCN_EALB', 'HRCN_EALA', 'HRCN_EALP',
                                                                 'RFLD_EALB', 'RFLD_EALA', 'RFLD_EALP',
                                                                 'BUILDVALUE', 'AGRIVALUE'])
    df['EAL'] = df['HRCN_EALB'] 
    df = df.drop(['HRCN_EALB', 'HRCN_EALA'], axis=1)

    # df['EALN'] = df['EAL'] / df['POPULATION']
    df['EAL'] = df['EAL'] / df['POPULATION']

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
 
    df = load_disasters_over_time(df) 
    
    df = load_dams_data(df)   
    
    # print("List of Inputs and Outputs")
    # print("~~~~~~~~")
    # for col in list(df.columns):
    #     print(f"{col}: {df[col].dtype}")

    # Remove extraneous states that do not get hurricanes
    fema_region_codes = {
        1: ["ME","VT","NH","MA","CT","RI"],
        2: ["NY", "NJ", "PR"],
        3: ["PA", "MD", "DE", "DC", "VA", "WV"],
        4: ["KY","NC","SC","GA","AL","MS","TN","FL"],
        6: ["OK", "AR", "LA", "TX", "NM"]
    }
    states = []
    for region in fema_region_codes.values():
        for state in region:
            states.append(state)
    
    df = df[df["STATEABBRV"].isin(states)]

    df.to_csv("output.csv", index=False)

if __name__ == "__main__":
    load_predicitve_data()