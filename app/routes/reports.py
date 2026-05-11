from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import os
import csv
import io
from dotenv import load_dotenv

load_dotenv()

reports_bp = Blueprint('reports', __name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


@reports_bp.route('/export', methods=['GET'])
@jwt_required()
def export_csv():
    try:
        user_id = get_jwt_identity()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT employee_number, age, department, job_role,
                   monthly_income, years_at_company, years_since_last_promotion,
                   overtime, job_satisfaction, attrition, risk_score, risk_level
            FROM employees
            WHERE user_id = %s
            ORDER BY risk_score DESC
        """, (user_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'Employee Number', 'Age', 'Department', 'Job Role',
            'Monthly Income', 'Years At Company', 'Years Since Last Promotion',
            'Overtime', 'Job Satisfaction', 'Attrition',
            'Risk Score', 'Risk Level'
        ])

        for row in rows:
            writer.writerow(row)

        output.seek(0)

        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=hr_attrition_report.csv'

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500