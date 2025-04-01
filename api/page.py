from flask import Flask, request, jsonify
from flask_cors import CORS


import torch
import pandas as pd
import ollama

import sys
import os

from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../predictive_model')))
from neural_network import Neural_Network

predictions = []
data = []
model = ""

app = Flask(__name__)
CORS(app)

@app.route("/man_predict")
def man_predict():
    global model
    population = float(request.args.get("population"))
    buildvalue = float(request.args.get("buildvalue"))
    hrcn_ealp = float(request.args.get("hrcn_ealp"))
    disaster_per_year_20 = float(request.args.get("disaster_per_year_20"))
    disaster_per_year_10 = float(request.args.get("disaster_per_year_10"))
    disaster_per_year_5 = float(request.args.get("disaster_per_year_5"))
    disaster_per_year_1 = float(request.args.get("disaster_per_year_1"))
    mean = float(request.args.get("mean"))
    count = float(request.args.get("count"))

    X = torch.tensor([population, buildvalue, hrcn_ealp,
                      disaster_per_year_20, disaster_per_year_10,
                      disaster_per_year_5, disaster_per_year_1,
                      mean, count])
    with torch.no_grad():  
        prediction = model(X)
    

    prompt = ""
    prompt += "You are a analyst/economist that helps predict the impact of hurricanes on local communities.\n"
    prompt += "You predict the property damage per person per year per county.\n"
    prompt += f"Your prediction for this year is that his county's damage per year per person per county is {prediction.item()}.\n"
    prompt += f"Your came to this conclusion through population is {population}, the value of all buildings in the county is {buildvalue}, "
    prompt += f"Estimated Loss of live per year is {hrcn_ealp}, average number of hurricanes per year for the last 20 years {disaster_per_year_20}, "
    prompt += f"average number of hurricanes per year for the last 10 years {disaster_per_year_10}, average number of hurricanes per year for the last 5 years {disaster_per_year_5}, "
    prompt += f"average number of hurricanes per year for the last year {disaster_per_year_1}, the average safety index of {mean}, and number of dams in this county are {count}.\n\n"
    prompt += f"Give a summary report of why you gave this ranking.\n"
    prompt += f"Respond only in the html format below.\n"

    prompt += """<div class="summary"><h2>The predicted damage per person per year in this county is ..., based on the following analysis:<h2>

<p><b>Population</b>: With a population of ... explain. {do this for all categories}</p> {each cat is on a new line}\n

These factors combined indicate that this county is at {blank} risk for significant property damage and disruption to daily life due to hurricanes.</div>"""
    response = ollama.chat(model='llama3.2:latest', messages=[{'role': 'user', 'content': prompt}])
    print(response)
    return jsonify({'prediction': prediction.item(), 'response': response['message']['content']})

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
    
    app.run(debug=True)