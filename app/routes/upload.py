from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from ..services.predictor import predict_attrition

load_dotenv()

upload_bp = Blueprint('upload', __name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


@upload_bp.route('/csv', methods=['POST'])
@jwt_required()
def upload_csv():
    try:
        user_id = get_jwt_identity()

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'}), 400

        df = pd.read_csv(file)

        required_columns = [
            'Age', 'Department', 'JobRole', 'MonthlyIncome',
            'YearsAtCompany', 'YearsSinceLastPromotion', 'OverTime',
            'JobSatisfaction', 'WorkLifeBalance', 'EnvironmentSatisfaction',
            'DistanceFromHome', 'NumCompaniesWorked', 'Attrition'
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            return jsonify({'error': f'Missing columns: {missing}'}), 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM employees WHERE user_id = %s", (user_id,))

        count = 0
        for _, row in df.iterrows():
            prediction = predict_attrition(row.to_dict())

            cur.execute("""
                INSERT INTO employees (
                    user_id, employee_number, age, department, job_role,
                    monthly_income, years_at_company, years_since_last_promotion,
                    overtime, job_satisfaction, attrition, risk_score, risk_level
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                int(row.get('EmployeeNumber', count + 1)),
                int(row['Age']),
                str(row['Department']),
                str(row['JobRole']),
                int(row['MonthlyIncome']),
                int(row['YearsAtCompany']),
                int(row['YearsSinceLastPromotion']),
                str(row['OverTime']),
                int(row['JobSatisfaction']),
                str(row['Attrition']),
                prediction['risk_score'],
                prediction['risk_level']
            ))
            count += 1

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'message': f'Successfully processed {count} employees',
            'count': count
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500