import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
from feature_engineering import create_features

# Load data
df = pd.read_csv("../data/telco_churn.csv")

if "customerID" in df.columns:
    df = df.drop("customerID", axis=1)

df = create_features(df)

X = df.drop("Churn", axis=1)
y = df["Churn"]

print(list(X.columns))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

print("F1 Score:", f1_score(y_test, pred))
print("ROC AUC:", roc_auc_score(y_test, proba))

joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")
