import pandas as pd

def create_features(df):
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.fillna(0, inplace=True)

    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    df = pd.get_dummies(df, drop_first=True)

    return df
