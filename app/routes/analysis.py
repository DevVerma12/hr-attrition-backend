from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import os
from dotenv import load_dotenv
from ..services.analyzer import get_overview, get_department_analysis, get_risk_distribution
from ..services.predictor import get_feature_importance

load_dotenv()

analysis_bp = Blueprint('analysis', __name__)

def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def fetch_employees(user_id, department=None, risk_level=None):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT employee_number, age, department, job_role,
               monthly_income, years_at_company, years_since_last_promotion,
               overtime, job_satisfaction, attrition, risk_score, risk_level
        FROM employees
        WHERE user_id = %s
    """
    params = [user_id]

    if department:
        query += " AND department = %s"
        params.append(department)

    if risk_level:
        query += " AND risk_level = %s"
        params.append(risk_level)

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    columns = [
        'employee_number', 'age', 'department', 'job_role',
        'monthly_income', 'years_at_company', 'years_since_last_promotion',
        'overtime', 'job_satisfaction', 'attrition', 'risk_score', 'risk_level'
    ]

    return [dict(zip(columns, row)) for row in rows]


@analysis_bp.route('/overview', methods=['GET'])
@jwt_required()
def overview():
    try:
        user_id = get_jwt_identity()
        employees = fetch_employees(user_id)
        data = get_overview(employees)
        distribution = get_risk_distribution(employees)
        data['risk_distribution'] = distribution
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/department', methods=['GET'])
@jwt_required()
def department():
    try:
        user_id = get_jwt_identity()
        employees = fetch_employees(user_id)
        data = get_department_analysis(employees)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/employees', methods=['GET'])
@jwt_required()
def employees():
    try:
        user_id = get_jwt_identity()
        department = request.args.get('department')
        risk_level = request.args.get('risk')
        data = fetch_employees(user_id, department, risk_level)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/factors', methods=['GET'])
@jwt_required()
def factors():
    try:
        data = get_feature_importance()
        return jsonify(data), 200
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500