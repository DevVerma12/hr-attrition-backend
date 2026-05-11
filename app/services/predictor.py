import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../models/attrition_model.pkl')

FEATURES = [
    'Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked',
    'YearsAtCompany', 'YearsSinceLastPromotion', 'JobSatisfaction',
    'WorkLifeBalance', 'EnvironmentSatisfaction', 'OverTime_Yes',
    'Department_Research & Development', 'Department_Sales'
]

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Please run train_model.py first.")
    return joblib.load(MODEL_PATH)


def predict_attrition(employee_data: dict) -> dict:
    model = load_model()

    df = pd.DataFrame([employee_data])

    df['OverTime_Yes'] = 1 if employee_data.get('OverTime') == 'Yes' else 0
    df['Department_Research & Development'] = 1 if employee_data.get('Department') == 'Research & Development' else 0
    df['Department_Sales'] = 1 if employee_data.get('Department') == 'Sales' else 0

    for col in FEATURES:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURES]

    risk_score = round(float(model.predict_proba(df)[0][1]) * 100, 2)

    if risk_score >= 60:
        risk_level = 'High'
    elif risk_score >= 30:
        risk_level = 'Medium'
    else:
        risk_level = 'Low'

    return {
        'risk_score': risk_score,
        'risk_level': risk_level
    }


def get_feature_importance() -> list:
    model = load_model()
    importances = model.feature_importances_

    result = []
    for feature, importance in zip(FEATURES, importances):
        result.append({
            'feature': feature,
            'importance': round(float(importance) * 100, 2)
        })

    return sorted(result, key=lambda x: x['importance'], reverse=True)