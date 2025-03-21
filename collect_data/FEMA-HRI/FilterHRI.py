import os
import json
import pandas as pd

fema_region_codes = {
    1: ["ME","VT","NH","MA","CT","RI"],
    2: ["NY", "NJ", "PR"],
    3: ["PA", "MD", "DE", "DC", "VA", "WV"],
    4: ["KY","NC","SC","GA","AL","MS","TN","FL"],
    6: ["OK", "AR", "LA", "TX", "NM"]
}

def apply_filter(df: pd.DataFrame) -> dict:
    """Remove extraneous states."""
    
    data = {}
    for region, states in fema_region_codes.items():
        filtered_df = df[df["STATEABBRV"].isin(states)]
        filtered_data = filtered_df.to_dict()
        json_data = filtered_df.to_json(orient="records", lines=False)
        # print(json_data)
        data[region] = json.loads(json_data)

    return data

def main():
    """Filter the unfiltered FEMA dataset."""

    """
    ****************************
    *      Error Checking      *
    ****************************
    """

    # Verify all_disasters.json exists and filtered_diasasters.json does not
    if not os.path.exists("raw_data/FEMA-HRI/all_counties.csv"):
        print("Error: all_counties.json does NOT exist")
        return
    if os.path.exists("raw_data/DisasterDeclarationsSummaries/filtered_counties.json"):
        print("Error: filtered_counties.json ALREADY exists")
        return


    """
    ****************************
    *       Apply Filter       *
    ****************************
    """

    # Load unfiltered dataset
    with open("raw_data/FEMA-HRI/all_counties.csv") as f:
        unfiltered_data = pd.read_csv(f)

    # Remove extraneous data
    data = apply_filter(unfiltered_data)
    # print(data)

    """
    ***************************
    *  filtered_counties.json *
    ***************************
    """

    # Write to filtered_disasters
    with open("raw_data/FEMA-HRI/filtered_counties.json", "w") as f:
        unfiltered_data = json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()


