import os
import json
import requests
"""Script to get all relevant disasters since last request."""

def get_disaster_date() -> str:
    """Gets date of the most recently retrieved natural disaster."""

    if not os.path.isfile("raw_data/DisasterDeclarationsSummaries/filtered_disasters.json"):
        return "N/A"

    # Open raw data
    with open("raw_data/DisasterDeclarationsSummaries/filtered_disasters.json") as f:
        data = json.loads(f.read())

    # Find most recent date
    most_recent_date = {"year": 0, "month": 1, "day": 1}
    date_str = ""
    for disaster in data["DisasterDeclarationsSummaries"]:
        year, month, day = disaster["declarationDate"].split("T")[0].split("-")
        
        if int(year) >= most_recent_date["year"]:
            most_recent_date = {"year": int(year), "month": int(month), "day": int(day)}
            date_str = disaster["declarationDate"]
        
        if int(month) >= most_recent_date["month"]:
            if int(year) >= most_recent_date["year"]:
                    most_recent_date = {"year": int(year), "month": int(month), "day": int(day)}
                    date_str = disaster["declarationDate"]
        
        if int(day) >= most_recent_date["day"]:
            if int(month) >= most_recent_date["month"]:
                if int(year) >= most_recent_date["year"]:
                        most_recent_date = {"year": int(year), "month": int(month), "day": int(day)}
                        date_str = disaster["declarationDate"]

    return date_str

def create_url(date: str) -> str:
    """Creates URL for api with filters."""

    # Relevant Disasters 
    disaster_codes = {
        "Hurricane": "\'H\'",
        "Dam/Levee Break": "\'K\'",
        "Flood": "\'F\'",
        "Severe Storm": "\'W\'",
        "Tropical Storm": "\'4\'",
        "Tropical Depression": "\'8\'"
    } 
    disasters = ",".join(list(disaster_codes.values())) 

    # Relevant Regions (check fema region map for more info)
    regions = str((1,2,3,4,6))


    # Concatenate all Filters into one string 
    filters = [f"region in ({regions})",f"designatedIncidentTypes in ({disasters})", f"declarationDate gt '{date}'"]
    filter = " and ".join(filters)
    # print(filter)
    # Request Data from FEMA 
    url = f"https://www.fema.gov/api/open/v2//DisasterDeclarationsSummaries?$filter={filter}"
    # print(url)
    return url

def update_database(new_data: dict) -> None:
    """Updates JSON file."""
    
    with open("raw_data/DisasterDeclarationsSummaries/test.json") as f:
        data = json.load(f)

    new_data["DisasterDeclarationsSummaries"].extend(data["DisasterDeclarationsSummaries"])

    with open("raw_data/DisasterDeclarationsSummaries/test.json", "w") as f:
        json.dump(new_data, f)

    return

def main():
    """Accesses the FEMA API to update our own database."""

    # Get most recent date
    last_diaster_date = get_disaster_date()
    if last_diaster_date == "N/A":
        print("Error: filtered_disasters.json NOT found")
        return

    # Create URL to get all new data
    url = create_url(date=last_diaster_date)
    response = requests.get(url)

    # Handle API response and add to json
    new_data = json.loads(response.content)
    if len(new_data["DisasterDeclarationsSummaries"]) == 0:
        print("No New Data Entries")
        return
    update_database(new_data)

if __name__ == "__main__":
    main()