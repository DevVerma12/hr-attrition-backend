def format_percentage(value):
    return round(float(value) * 100, 2)

def get_risk_level(score):
    if score >= 60:
        return 'High'
    elif score >= 30:
        return 'Medium'
    return 'Low'