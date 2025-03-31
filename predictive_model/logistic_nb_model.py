import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processed_data.preprocess import load_predicitve_data



#import data from preporcess script here instead of df
df = load_predicitve_data()

import torch
from torch import tensor
from torch.optim import SGD
from torch import floor

#convert data to tensors so that pytorch can operate it
X = df[["POPULATION", "BUILDVALUE", "AGRIVALUE", "DISASTER_PER_YEAR_20", "DISASTER_PER_YEAR_10", 
        "DISASTER_PER_YEAR_5", "DISASTER_PER_YEAR_1", "mean", "count"]]
X = torch.tensor(X.values)
y = tensor(df["EAL"], dtype=torch.float)
y = (y >= 1) * 1.

from torch import sigmoid

#check logistic loss
def log_loss(h,y):
    L = -y * torch.log(h) - (1-y) * torch.log(1-h)
    J = L.mean()
    return J

from torch.nn import Module, Parameter
from torch.distributions.normal import Normal

class Logistic (Module):
    #constructor
    def __init__ (self):
        Module.__init__(self)
        self.w = Parameter(Normal(0., 0.1).sample((1,)).requires_grad_())
        self.b = Parameter(tensor(0., dtype = torch.float).requires_grad_())
    #sigmoid calculation
    def forward (self, X):
        z = X @ self.w + self.b
        h = sigmoid(z)
        return h
    
#check how accurate the model is to df(won't apply to us)
def accuracy(h,y):
    yhat = floor(h + 0.5)
    return ((yhat == y) * 1.).mean()
#the whole process to do a step forward
def step (model, X, y, lossf, optz):
    h = model(X)
    J = lossf(h, y)
    print("J: ", J, "acc: ", accuracy(h,y))
    J.backward()
    optz.step()
    model.zero_grad()
#train the model
def train (X, y, stepsize, nepochs):
    model = Logistic()
    sgd = SGD(model.parameters(), lr=stepsize)
    for _ in range(nepochs):
        step(model, X, y, log_loss, sgd)
    return model


if __name__ == "__main__":

    model = Logistic()

    model(X)

    J = log_loss(model(X), y)
    """
    print(model.w)
    print(model.b)
    print(list(model.parameters()))
    print(dict(model.named_parameters()))
    print(model.w.data)
    print(model.w)
    """

    J.backward()

    print(model.w.grad)
    print(model.b.grad)

    sgd = SGD(model.parameters(), lr = 0.01)
    """
    print(model.w.data - 0.01 * model.w.grad)
    print(model.b)
    print(model.w)
    print(sgd.step())
    print(model.w)
    print(model.b)
    print(model.w.data)
    print(model.w.grad)
    print(model.zero_grad())
    print(model.w.grad)
    print(model.b.grad)
    """

    step(model, X, y, log_loss, sgd)
    step(model, X, y, log_loss, sgd)
    print(model.w)
    
    h = model(X)
    print(h)
    print(floor(h + 0.5))
    print(accuracy(h,y))

    train(X, y, 0.001, 1000)
