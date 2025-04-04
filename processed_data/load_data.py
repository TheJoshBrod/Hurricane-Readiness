import os
import io
import re
import json
import shutil
import zipfile
import requests
import pandas as pd

def fetch_and_filter_fema_disasters():
    disaster_codes = {"H": "Hurricane", "K": "Dam/Levee Break", "F": "Flood", "W": "Severe Storm", "4": "Tropical Storm", "8": "Tropical Depression"}
    disasters = ",".join([f"'{code}'" for code in disaster_codes.keys()])
    regions = "(1,2,3,4,6)"
    filters = [f"region in {regions}", f"designatedIncidentTypes in ({disasters})"]
    filter_str = " and ".join(filters)
    url = f"https://www.fema.gov/api/open/v2//DisasterDeclarationsSummaries?$filter={filter_str}"

    response = requests.get(url)
    raw_data = response.json()
    data = []

    for disaster in raw_data["DisasterDeclarationsSummaries"]:
        area = disaster["designatedArea"].lower()
        if "county" not in area:
            continue
        disaster["designatedArea"] = re.sub(r'\s?\(county\)$', '', area).capitalize()

        code = disaster.get("designatedIncidentTypes")
        if code not in disaster_codes and code is not None:
            keywords = ["hurricane", "dam", "flood", "water", "rain"]
            if not any(kw in (disaster.get("incidentType", "") + disaster.get("declarationTitle", "")).lower() for kw in keywords):
                continue

        if disaster["region"] not in [1, 2, 3, 4, 6]:
            continue

        data.append(disaster)

    output_path = os.path.join("raw_data", "FEMA-DDS", "filtered_disasters.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump({"DisasterDeclarationSummaries": data}, f, indent=4)


def fetch_and_filter_county_data():
    url = 'https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_Table_Counties/NRI_Table_Counties.zip'
    folder_path = 'NRI_Data'
    
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(folder_path)

    df = pd.read_csv(os.path.join(folder_path, 'NRI_Table_Counties.csv'))
    

    fema_region_codes = {
        1: ["ME", "VT", "NH", "MA", "CT", "RI"],
        2: ["NY", "NJ", "PR"],
        3: ["PA", "MD", "DE", "DC", "VA", "WV"],
        4: ["KY", "NC", "SC", "GA", "AL", "MS", "TN", "FL"],
        6: ["OK", "AR", "LA", "TX", "NM"]
    }

    data = {}
    for region, states in fema_region_codes.items():
        filtered_df = df[(df["STATEABBRV"].isin(states)) & (df["COUNTYTYPE"] == "County")]
        json_data = filtered_df.to_json(orient="records")
        data[region] = json.loads(json_data)

    shutil.rmtree(folder_path)

    output_path = os.path.join("raw_data", "FEMA-HRI", "filtered_counties.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def download_dam_csv():
    url = "https://nid.sec.usace.army.mil/api/nation/csv"
    output_path = os.path.join("raw_data", "Dams", "nation.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    response = requests.get(url)
    lines = response.text.splitlines()

    # Skip the first row (metadata)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines[1:]))  # Write all but the first line


def main():
    fetch_and_filter_fema_disasters()
    fetch_and_filter_county_data()
    download_dam_csv()

if __name__ == "__main__":
    main()