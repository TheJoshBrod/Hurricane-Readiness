from flask import Flask, request, jsonify
from flask_cors import CORS

import json

import torch
import pandas as pd
import ollama

import sys
import os

from urllib.parse import unquote

from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../predictive_model')))
from neural_network import Neural_Network

predictions = []
data = []
model = ""

app = Flask(__name__)
CORS(app)


def generate_json_params(query: str):
    try: 
        prompt = "You are a weather and climate analyst whose job is to analyze hurricane risk over time\n"
        prompt += "A local member of your community asks for an assessment of the risk of the community.\n"
        prompt += "They come to you with the following info:\n"
        prompt += query + "\n"
        prompt += "You have a Neural net that takes in certain inputs to estimate the building damage/year occur due to hurricanes\n"
        prompt += "It requires the following information\n"
        prompt += """
                    population: population of this county.
                    buildvalue: estimated vallue of all building properties in this county.
                    hrcn_ealp: estimated loss of life per year due to hurricanes in this county.
                    disaster_per_year_20: estimated number of hurricanes that have hit this county in the last 20 years.
                    disaster_per_year_10: estimated number of hurricanes that have hit this county in the last 10 years.
                    disaster_per_year_5: estimated number of hurricanes that have hit this county in the last 5 years.
                    disaster_per_year_1: estimated number of hurricanes that have hit this county in the last year.
                    mean: Average Dam saftey index score
                    count: number of dams in the county
                """
        prompt += """
                    Please only respond in the following json format:
                    {
                    "population":<value>
                    ...
                    }
                    """
        response = ollama.chat(model='llama3.2:latest', messages=[{'role': 'user', 'content': prompt}])['message']['content']
    except Exception as e:
        print(e)
        response = generate_json_params(query)
    return json.loads(response)

@app.route("/auto_predict")
def auto_predict():
    global model
    print("Begining auto predict")
    user_response = unquote(request.args.get("query"))
    params = generate_json_params(user_response)
    
    print("Generated estimates")
    print(params)

    X = torch.tensor([float(params["population"]),
                      float(params["buildvalue"]),
                      float(params["hrcn_ealp"]),
                      float(params["disaster_per_year_20"]),
                      float(params["disaster_per_year_10"]),
                      float(params["disaster_per_year_5"]),
                      float(params["disaster_per_year_1"]),
                      float(params["mean"]),
                      float(params["count"])])
    with torch.no_grad():  
        prediction = model(X)
    print(f"Predicted value is {prediction.item()}")

    
    print("Generating summary report")
    prompt = ""
    prompt += "You are a analyst/economist that helps predict the impact of hurricanes on local communities.\n"
    prompt += "You predict the property damage per person per year per county.\n"
    prompt += f"Your prediction for this year is that his county's damage per year per person per county is {prediction.item()}.\n"
    prompt += f"Your came to this conclusion through a local citizen coming to you with a description of your county.\n"
    prompt += f"You had to estimate each of the following piece of information below\n"
    prompt += f"Estimated population is {params["population"]}, Estimated value of all buildings in the county is {params["buildvalue"]}, "
    prompt += f"Estimated Loss of live per year is {params["hrcn_ealp"]}, Estimated average number of hurricanes per year for the last 20 years {params["disaster_per_year_20"]}, "
    prompt += f"Estimated average number of hurricanes per year for the last 10 years {params["disaster_per_year_10"]}, Estimated average number of hurricanes per year for the last 5 years {params["disaster_per_year_5"]}, "
    prompt += f"Estimated average number of hurricanes per year for the last year {params["disaster_per_year_1"]}, the Estimated average safety index of {params["mean"]}, and Estimated number of dams in this county are {params["count"]}.\n\n"
    prompt += f"Give a summary report of why you gave this ranking and why u estimated each value.\n"
    prompt += f"Respond only in the html format below.\n"

    prompt += """<div class="summary"><h2>The predicted damage per person per year in this county is ..., based on the following analysis:<h2>

<p><b>Population</b>: With a population of ... explain. {do this for all categories}</p> {each cat is on a new line}\n

These factors combined indicate that this county is at {blank} risk for significant property damage and disruption to daily life due to hurricanes.</div>"""
    response = ollama.chat(model='llama3.2:latest', messages=[{'role': 'user', 'content': prompt}])
    print(response['message']['content'])
    return jsonify({'prediction': prediction.item(), 'response': response['message']['content']})


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
    print(response['message']['content'])
    return jsonify({'prediction': prediction.item(), 'response': response['message']['content']})

@app.route("/")
def homepage():
    global data
    global predictions
    state = request.args.get("state")

    filtered_data = data[data["STATEABBRV"] == state][["STATE","COUNTY","Predicted EAL/Population", "Actual EAL"]]
    filtered_data = filtered_data.rename(columns={'Predicted EAL/Population': 'Predicted EAL'})
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