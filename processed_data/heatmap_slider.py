import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


def generate_legend(data_column, output_path, cmap='OrRd', num_ticks=6):
    import matplotlib as mpl

    # Load data for this column 
    data = pd.read_csv("processed_data/data.csv")
    values = data[data_column].dropna()

    if values.empty:
        print(f"No values found for {data_column}, skipping legend.")
        return

    # Create a dummy colorbar 
    fig, ax = plt.subplots(figsize=(5, 1))
    fig.subplots_adjust(bottom=0.5)

    norm = mpl.colors.Normalize(vmin=values.min(), vmax=values.max())
    cb = mpl.colorbar.ColorbarBase(
        ax,
        cmap=plt.get_cmap(cmap),
        norm=norm,
        orientation='horizontal',
        ticks=np.linspace(values.min(), values.max(), num_ticks)
    )

    if data_column == "EAL":
        cb.set_label("Expected Annual Loss Per Person")

    elif data_column == "EALNN":
        cb.set_label("Total Expected Annual Loss")

    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


def generate_heatmap(state_fips, data_column, output_filename, output_dir="heatmap_images"):


    # Load your CSV 
    data = pd.read_csv("processed_data/data.csv")
    data['STATEFIPS'] = data['STATEFIPS'].astype(str).str.zfill(2)
    data['COUNTYFIPS'] = data['COUNTYFIPS'].astype(str).str.zfill(3)
    data['FIPS'] = data['STATEFIPS'] + data['COUNTYFIPS']

    # Filter by selected state 
    state_data = data[data['STATEFIPS'] == state_fips]

    # Load US counties and filter to selected state 
    shapefile_url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_5m.zip"
    counties = gpd.read_file(shapefile_url)
    counties = counties[counties['STATEFP'] == state_fips]
    counties['GEOID'] = counties['GEOID'].astype(str).str.zfill(5)

    # Merge and split data 
    merged = counties.merge(state_data, how='left', left_on='GEOID', right_on='FIPS')

    # Skip if merged GeoDataFrame is empty or has no geometry 
    if merged.empty or merged.geometry.isnull().all():
        print(f"Skipping {state_fips} — no valid geometries.")
        return

    data_counties = merged[merged[data_column].notnull()]
    outline_only = merged[merged[data_column].isnull()]

    # Plot 
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=300)

    if not outline_only.empty:
        outline_only.plot(
            ax=ax,
            facecolor="none",
            edgecolor="lightgray",
            linewidth=0.5
        )

    if not data_counties.empty:
        data_counties.plot(
            column=data_column,
            cmap='OrRd',
            linewidth=0.5,
            edgecolor='black',
            legend=False,
            ax=ax
        )

    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Save the image in the specified directory 
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()

def main():
    output_dir = os.path.join("assets", "heatmap_images")
    os.makedirs(output_dir, exist_ok=True)

    data = pd.read_csv("processed_data/data.csv")
    data['STATEFIPS'] = data['STATEFIPS'].astype(str).str.zfill(2)
    data['COUNTYFIPS'] = data['COUNTYFIPS'].astype(str).str.zfill(3)
    data['FIPS'] = data['STATEFIPS'] + data['COUNTYFIPS']

    state_fips_list = data['STATEFIPS'].unique()

    for state_fips in state_fips_list:
        state_data = data[data['STATEFIPS'] == state_fips]
        num_counties_with_eal = state_data['EAL'].notnull().sum()
        num_counties_with_ealnn = state_data['EALNN'].notnull().sum()

        if num_counties_with_eal > 1 and num_counties_with_ealnn > 1:
            generate_heatmap(state_fips, 'EAL', f"{state_fips}_eal_n.png", output_dir=output_dir)
            generate_heatmap(state_fips, 'EALNN', f"{state_fips}_eal_nn.png", output_dir=output_dir)
        else:
            print(f"Skipping {state_fips} — not enough data.")

    generate_legend('EAL', os.path.join(output_dir, "legend_n.png"))
    generate_legend('EALNN', os.path.join(output_dir, "legend_nn.png"))



if __name__ == "__main__":
    main()
