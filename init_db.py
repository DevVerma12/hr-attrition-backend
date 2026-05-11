import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print("Connecting to DB...")
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

print("Creating tables...")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS employees (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  employee_number INTEGER,
  age INTEGER,
  department VARCHAR(100),
  job_role VARCHAR(100),
  monthly_income INTEGER,
  years_at_company INTEGER,
  years_since_last_promotion INTEGER,
  overtime VARCHAR(10),
  job_satisfaction INTEGER,
  work_life_balance INTEGER,
  environment_satisfaction INTEGER,
  distance_from_home INTEGER,
  num_companies_worked INTEGER,
  attrition VARCHAR(10),
  risk_score FLOAT,
  risk_level VARCHAR(20),
  uploaded_at TIMESTAMP DEFAULT NOW()
);
""")

conn.commit()
cur.close()
conn.close()
print("Tables created successfully")
