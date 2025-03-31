import sys
import os
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

# load data from preprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from processed_data.preprocess import load_predicitve_data
df = load_predicitve_data()
df = df.dropna()
#X = df[["POPULATION", "DISASTER_PER_YEAR_20"]]
scaler = StandardScaler()
columns = ["POPULATION", "BUILDVALUE", "AGRIVALUE", 
        "DISASTER_PER_YEAR_20", "mean", "count"]
df[columns] = scaler.fit_transform(df[columns])
X = df[columns]
Y = df['EAL']

# build model
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()

print(model.summary())