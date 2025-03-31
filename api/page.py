from flask import Flask, request
from flask_cors import CORS


import torch
import pandas as pd

import sys
import os

from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../predictive_model')))
from neural_network import Neural_Network

predictions = []
data = []

app = Flask(__name__)
CORS(app)


@app.route("/")
def homepage():
    global data
    global predictions
    state = request.args.get("state")

    filtered_data = data[data["STATEABBRV"] == state][["STATE","COUNTY","Predicted EAL/Population", "Actual EAL"]]
    
    return filtered_data.to_html(index=False)


if __name__ == "__main__":
    model = torch.load("predictive_model/model.pth", weights_only=False)
    model.eval()

    df = pd.read_csv("processed_data/data.csv")
    df = df.dropna()
    scaler = StandardScaler()
    columns = ["POPULATION", "BUILDVALUE", 'HRCN_EALP',
            #    'RFLD_EALB', 'RFLD_EALA', 'RFLD_EALP',
            "DISASTER_PER_YEAR_20", "DISASTER_PER_YEAR_10", "DISASTER_PER_YEAR_5", "DISASTER_PER_YEAR_1",
            "mean", "count"]
    print("~~~~~\n\n\n")
    print(df.head())
    df[columns] = scaler.fit_transform(df[columns])

  
    X = torch.tensor(df[columns].values, dtype=torch.float32)
    with torch.no_grad():  
        predictions = model(X)
        numpy_array = predictions.numpy()
        predictions = pd.DataFrame(numpy_array, columns=['Estimated EAL/Population'])

    data = df[["STATE", "COUNTY", "STATEABBRV"]]
    if len(data) == len(predictions):
        # Add predictions as a new column to the data DataFrame
        data['Predicted EAL/Population'] = predictions['Estimated EAL/Population']
    else:
        print(f"Error: Length mismatch - data has {len(data)} rows, predictions has {len(predictions)} rows")
    data = data.sort_values(by='Predicted EAL/Population', ascending=False, inplace=False)
    data["Actual EAL"] = df["EAL"]
    # print(data.head())
    app.run(debug=True)