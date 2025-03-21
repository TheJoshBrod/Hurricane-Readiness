import os
import json
"""Creates Filtered Disasters JSON file"""

def apply_filter(raw_data: dict) -> dict:
    
    data = []
    for disaster in raw_data["DisasterDeclarationsSummaries"]:
        
        designated_incident_types = {
            "Hurricane": "H",
            "Dam/Levee Break": "K",
            "Flood": "F",
            "Severe Storm": "W",
            "Tropical Storm": "4",
            "Tropical Depression": "8"
        }
        disaster_codes = list(designated_incident_types.values())
        if disaster["designatedIncidentTypes"] not in disaster_codes:
            if disaster["designatedIncidentTypes"] != None:
                continue

            # Checks if dataset is missing designatedIncidentType, if any other hints that its relevant
            found_keyword = False
            keywords = ["hurricane","dam","flood","water","rain"]
            for word in keywords: 
                if word in disaster["incidentType"].lower():
                    found_keyword = True
                    break
                if word in disaster["declarationTitle"].lower():
                    found_keyword = True
                    break

            if not found_keyword:
                continue

        # East Coast and South (see fema_regions_map.png for more info)
        regions = (1,2,3,4,6)
        if disaster["region"] > 4 and disaster["region"] != 6:
            continue 

        data.append(disaster)
    
    output = {"DisasterDeclarationSummaries": data}
    return output

def main():
    """Filter the unfiltered FEMA dataset."""

    """
    ***************************
    *      Error Checking     *
    ***************************
    """

    # Verify all_disasters.json exists and filtered_diasasters.json does not
    if not os.path.exists("raw_data/DisasterDeclarationsSummaries/all_disasters.json"):
        print("Error: all_disasters.json does NOT exist")
        return
    if os.path.exists("raw_data/DisasterDeclarationsSummaries/filtered_disasters.json"):
        print("Error: filtered_disasters.json ALREADY exists")
        return



    """
    ***************************
    *       Apply Filter      *
    ***************************
    """

    # Load unfiltered dataset
    with open("raw_data/DisasterDeclarationsSummaries/all_disasters.json") as f:
        unfiltered_data = json.load(f)

    # Remove extraneous data
    data = apply_filter(unfiltered_data)


    """
    ***************************
    * filtered_disasters.json *
    ***************************
    """

    # Write to filtered_disasters
    with open("raw_data/DisasterDeclarationsSummaries/filtered_disasters.json", "w") as f:
        unfiltered_data = json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()