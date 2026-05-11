import pandas as pd

def get_overview(employees):
    df = pd.DataFrame(employees)

    if df.empty:
        return {
            'total_employees': 0,
            'attrition_count': 0,
            'attrition_rate': 0,
            'avg_age': 0,
            'avg_income': 0
        }

    attrition_count = len(df[df['attrition'] == 'Yes'])
    attrition_rate = round((attrition_count / len(df)) * 100, 2)
    avg_age = round(df['age'].mean(), 1)
    avg_income = round(df['monthly_income'].mean(), 2)

    return {
        'total_employees': len(df),
        'attrition_count': attrition_count,
        'attrition_rate': attrition_rate,
        'avg_age': avg_age,
        'avg_income': avg_income
    }


def get_department_analysis(employees):
    df = pd.DataFrame(employees)

    if df.empty:
        return []

    dept_group = df.groupby('department')
    result = []

    for dept, group in dept_group:
        total = len(group)
        attrition = len(group[group['attrition'] == 'Yes'])
        rate = round((attrition / total) * 100, 2)
        avg_risk = float(group['risk_score'].mean()) if 'risk_score' in group.columns else 0.0
        result.append({
            'department': dept,
            'total_employees': total,
            'attrition_count': attrition,
            'attrition_rate': rate,
            'avg_risk_score': avg_risk
        })

    return sorted(result, key=lambda x: x['attrition_rate'], reverse=True)


def get_risk_distribution(employees):
    df = pd.DataFrame(employees)

    if df.empty:
        return {'High': 0, 'Medium': 0, 'Low': 0}

    distribution = df['risk_level'].value_counts().to_dict()
    return {
        'High': distribution.get('High', 0),
        'Medium': distribution.get('Medium', 0),
        'Low': distribution.get('Low', 0)
    }