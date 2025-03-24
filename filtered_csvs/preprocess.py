import pandas as pd
import torch

# File paths (update these if needed)
file_paths = {
    "NRI_HRCN_FLD_RISKS": "NRI_HRCN_FLD_RISKS.csv"
}

### Step 1: Load Data
def load_data(file_path):
    """Loads a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)

df_risks = load_data(file_paths["NRI_HRCN_FLD_RISKS"])

### Step 2: Preprocess Risk Data
def preprocess_risks(df):
    """Normalizes risk scores and extracts relevant columns."""
    risk_columns = ["NRI_ID", "HRCN 2024", "RFLD 2024", "Combined 2024"]
    df[risk_columns] = df[risk_columns] #.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    return df[["State", "County"] + risk_columns]

df_risks = preprocess_risks(df_risks)

### Step 4: Convert Data to PyTorch Tensors
def df_to_tensor(df, dtype=torch.float):
    """Converts a Pandas DataFrame to a PyTorch Tensor."""
    return torch.tensor(df.dropna().select_dtypes(include=['number']).values, dtype=dtype)

# Convert risk data
tensor_risks = df_to_tensor(df_risks)

### Step 5: Print Tensor Information
print("Risk Data Tensor Shape:", tensor_risks.shape)
print("Risk Data Tensor:", tensor_risks)
