import os
import shutil
import requests
import zipfile
import io
import pandas as pd

def load_fema_data():
    folder_path = 'NRI_Data'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    url = 'https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_Table_Counties/NRI_Table_Counties.zip'
    response = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall('NRI_Data')  # Extracts to a directory named 'NRI_Data'

    # Read the CSV file from the URL
    df = pd.read_csv('NRI_Data/NRI_Table_Counties.csv', usecols=['COUNTY', 'STATE', 'POPULATION', 'HRCN_EALB', 'HRCN_EALA'])
    df['EAL'] = df['HRCN_EALB'] + df['HRCN_EALA']
    df = df.drop(['HRCN_EALB', 'HRCN_EALA'], axis=1)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    return df
