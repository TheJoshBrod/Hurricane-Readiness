import geopandas as gpd
import json
import os

# Replace with your actual file path
FILE_PATH = "collect_data/Dams/nation.gpkg"
OUTPUT_JSON = "filtered_dams.json"

# Load GeoPackage
def load_dataset(file_path):
    print("📦 Loading GeoPackage...")
    return gpd.read_file(file_path)

# Filter dam-related records
def filter_dams(df):
    dam_keywords = ["dam"]
    dam_mask = df.apply(lambda row: row.astype(str).str.contains('|'.join(dam_keywords), case=False).any(), axis=1)
    return df[dam_mask]

# Export in FEMA-like structure
def export_to_json(df, output_path):
    records = []
    for _, row in df.iterrows():
        record = {
            "damName": row.get("DAM_NAME", "Unknown"),
            "state": row.get("STATE", "Unknown"),
            "county": row.get("COUNTY", "Unknown"),
            "yearCompleted": row.get("YEAR_COMPLETED", None),
            "hazardPotential": row.get("HAZARD", "Unknown"),
            "longitude": row.geometry.x if row.geometry else None,
            "latitude": row.geometry.y if row.geometry else None,
        }
        records.append(record)

    structured_output = {
        "DamSummaries": records
    }

    with open(output_path, "w") as f:
        json.dump(structured_output, f, indent=2)

    print(f"Exported {len(records)} formatted dam records to '{output_path}'")

# Main
def main():
    df = load_dataset(FILE_PATH)
    dam_df = filter_dams(df)
    export_to_json(dam_df, OUTPUT_JSON)

if __name__ == "__main__":
    main()
