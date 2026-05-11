import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv/WA_Fn-UseC_-HR-Employee-Attrition.csv')

df['Attrition'] = (df['Attrition'] == 'Yes').astype(int)
df['OverTime_Yes'] = (df['OverTime'] == 'Yes').astype(int)
df['Department_Research & Development'] = (df['Department'] == 'Research & Development').astype(int)
df['Department_Sales'] = (df['Department'] == 'Sales').astype(int)

FEATURES = [
    'Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked',
    'YearsAtCompany', 'YearsSinceLastPromotion', 'JobSatisfaction',
    'WorkLifeBalance', 'EnvironmentSatisfaction', 'OverTime_Yes',
    'Department_Research & Development', 'Department_Sales'
]

X = df[FEATURES]
y = df['Attrition']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

print("\nFeature Importances:")
for feat, imp in sorted(zip(FEATURES, model.feature_importances_), key=lambda x: x[1], reverse=True):
    print(f"  {feat}: {imp:.4f}")

os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/attrition_model.pkl')
print("\nModel saved to models/attrition_model.pkl")