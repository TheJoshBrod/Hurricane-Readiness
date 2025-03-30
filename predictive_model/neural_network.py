import os
import sys
import torch
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class Neural_Network(torch.nn.Module):
    def __init__(self) -> None:
        """Define model architecture."""
        super().__init__()
        self.sequence = torch.nn.Sequential(
                                        torch.nn.Linear(in_features=9, out_features=16, bias=True),
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

if __name__ == "__main__":
    # Load Data
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from preprocess import load_predicitve_data
    df = load_predicitve_data()
    df = df.dropna()
    scaler = StandardScaler()
    columns = ["POPULATION", "BUILDVALUE", "AGRIVALUE", 
            "DISASTER_PER_YEAR_20", "DISASTER_PER_YEAR_10", "DISASTER_PER_YEAR_5", "DISASTER_PER_YEAR_1", "mean", "count"]
    df[columns] = scaler.fit_transform(df[columns])

    # Split data for X,y
    X = torch.tensor(df[columns].values, dtype=torch.float32)
    y = torch.tensor(df["EAL"].values, dtype=torch.float32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
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