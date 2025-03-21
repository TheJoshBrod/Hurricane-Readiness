import pandas as pd
import json

# Read the CSV file, skipping the first row with metadata.
df = pd.read_csv("nation.csv", skiprows=1)

# Define the relevant columns from the CSV.
relevant_columns = [
    "Dam Name",
    "NID ID",
    "Primary Purpose",
    "Latitude",
    "Longitude",
    "State",
    "County",
    "City",
    "Year Completed",
    "Website URL"
]

# Filter the DataFrame to only include the relevant columns.
filtered_df = df[relevant_columns]

# Convert the filtered DataFrame to a list of dictionaries.
dam_data = filtered_df.to_dict(orient="records")

with open("dam_data.json", "w") as json_file:
    json.dump(dam_data, json_file, indent=4)

print("JSON file 'dam_data.json' created successfully!")

