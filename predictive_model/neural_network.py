import os
import sys
import torch
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import joblib

class Neural_Network(torch.nn.Module):
    def __init__(self) -> None:
        """Define model architecture."""
        super().__init__()
        self.sequence = torch.nn.Sequential(
                                        torch.nn.Linear(in_features=9, out_features=16, bias=True),
                                        torch.nn.ReLU(),
                                        torch.nn.Linear(in_features=16, out_features=16, bias=True),
                                        torch.nn.ReLU(),
                                        torch.nn.Linear(in_features=16, out_features=16, bias=True),
                                        torch.nn.ReLU(),
                                        torch.nn.Linear(in_features=16, out_features=16, bias=True),
                                        torch.nn.ReLU(),
                                        torch.nn.Linear(in_features=16, out_features=1, bias=True)
                                        )
        self.init_weights()
        

    def init_weights(self) -> None:
        """Initialize weights for each layer"""
        for layer in self.sequence:
            if isinstance(layer, torch.nn.Linear):  # Only initialize Linear layers
                torch.nn.init.xavier_uniform_(layer.weight)
                torch.nn.init.zeros_(layer.bias)

    def forward(self, x):
        """Forward pass"""
        output = self.sequence(x)
        return output
        
def train_nn(model: Neural_Network, X_train, y_train, optimizer, criterion, epochs=1000):
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs.squeeze(), y_train)
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs}, Loss: {loss.item()}")
"AGRIVALUE", 
if __name__ == "__main__":
    # Load Data
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # from processed_data.preprocess import load_predicitve_data
    # df = load_predicitve_data()
    df = pd.read_csv("processed_data/data.csv")
    df["county_state"] = df["COUNTY"] + ", " + df["STATE"]
    location = df["county_state"].values
    
    df = df.dropna()
    scaler = StandardScaler()
    columns = ["POPULATION", "BUILDVALUE", 'HRCN_EALP',
            "DISASTER_PER_YEAR_20", "DISASTER_PER_YEAR_10", "DISASTER_PER_YEAR_5", "DISASTER_PER_YEAR_1",
            "mean", "count"]
    print("~~~~~\n\n\n")
    print(df.head())
    df[columns] = scaler.fit_transform(df[columns])
    joblib.dump(scaler, 'scaler.pkl')
    # Split data for X,y
    X = torch.tensor(df[columns].values, dtype=torch.float32)
    y = torch.tensor(df["EAL"].values, dtype=torch.float32)

    X_train, X_test, y_train, y_test, location_train, location_test = train_test_split(X, y, location, test_size=0.2)

    # Output actual list
    sorted_data = sorted(zip(y_test, location_test), key=lambda x: x[0], reverse=True)
    with open("list.txt", "w") as f:
        for label, location in sorted_data:
            f.write(f"Location: {location}, Label: {label}\n")
    
    # Create model
    model = Neural_Network()
    for name, param in model.named_parameters():
        print(name, param.shape)

    # Set hyper parameters 
    params = model.parameters()
    learning_rate = 1e-3
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(params=params, lr=learning_rate, weight_decay=0.01)

    train_nn(model, X_train, y_train, optimizer, criterion)
    print("Finished training!")


    # Calculate performance
    with torch.no_grad():  
        predictions = model(X_test)

   
    predictions = predictions.squeeze() 
    predictions = predictions.cpu().numpy()
    y_test = y_test.cpu().numpy()

    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print(f'Mean Squared Error: {mse:.4f}')
    print(f'Root Mean Squared Error: {rmse:.4f}')
    print(f'R² (Coefficient of Determination): {r2:.4f}')
    torch.save(model, "predictive_model/model.pth")

    # Output predicted list
    sorted_data = sorted(zip(predictions, location_test), key=lambda x: x[0], reverse=True)
    with open("predicted_list.txt", "w") as f:
        for label, location in sorted_data:
            f.write(f"Location: {location}, Label: {label}\n")

            