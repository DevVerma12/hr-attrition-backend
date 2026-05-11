# 🎯 Interview Preparation Guide
## Project: HR Attrition Analysis & Prediction System

---

## 1. PROJECT INTRODUCTION

### ⏱ 30-Second Version
> *"I built a full-stack HR Attrition Analysis web application. It allows HR managers to upload their employee data as a CSV file, and the system automatically predicts which employees are at risk of leaving the company using a Machine Learning model. The dashboard shows attrition rates by department, risk score distributions, and key factors driving attrition — all in real time. It's built with React on the frontend, Flask on the backend, PostgreSQL as the database, and a Random Forest classifier for predictions."*

---

### ⏱ 1-Minute Version
> *"I built a full-stack HR Attrition Analysis and Prediction System. The core problem it solves is that companies often don't know which employees are likely to quit until it's too late. My application gives HR teams early warning by analyzing employee data and predicting attrition risk.*
>
> *Here's how it works: An HR manager logs in, uploads a CSV file of employee records, and the system instantly runs each employee through a trained Machine Learning model — a Random Forest classifier — which assigns a risk score and a risk level of High, Medium, or Low to every employee.*
>
> *The dashboard then visualizes everything: total employees, attrition rate, department-wise breakdown, and risk distribution. There's also an Employee Explorer where you can filter by department or risk level, and a Reports page where you can export the processed data back as a CSV.*
>
> *The stack is React with Vite on the frontend, Flask REST API on the backend, PostgreSQL for the database, and scikit-learn for the ML model. Authentication is done using JWT tokens with bcrypt password hashing."*

---

### ⏱ 2-Minute Version
> *"I built a full-stack HR Attrition Analysis and Prediction System. Let me walk you through what it does and how I built it.*
>
> *The problem I wanted to solve is a very real business problem: employee attrition is expensive. Studies show it costs between 50% to 200% of an employee's annual salary to replace them. Most companies react to resignations rather than preventing them. My project gives HR managers a proactive tool.*
>
> *The way it works is: an HR manager creates an account, logs in, and uploads a CSV file containing employee records — things like age, department, monthly income, job satisfaction, overtime hours, and so on. The backend validates the file, then for each employee row, it runs a prediction using a Random Forest model I trained on the IBM HR Analytics dataset — which is a well-known benchmark dataset in this domain.*
>
> *The model was trained on 12 features including age, income, years at company, overtime, job satisfaction, and department. It outputs a probability score between 0 and 100. I then bucket that into three levels: above 60 is High risk, 30 to 60 is Medium, below 30 is Low. All of this gets saved to PostgreSQL under the user's account.*
>
> *The React dashboard then shows KPI cards for total employees, attrition count, attrition rate, and average income. There are charts for department-wise attrition, risk distribution, and a feature importance section showing which factors matter most. You can filter employees by department or risk level and export a report as a CSV.*
>
> *The backend is a Flask REST API with four blueprints: auth, upload, analysis, and reports. Authentication uses JWT with bcrypt. The frontend uses Axios for API calls and React Context for auth state management.*
>
> *It was a complete end-to-end project that I built from scratch — from designing the database schema, training the ML model, building the REST API, to building the full React UI."*

---

## 2. FULL PROJECT EXPLANATION

### What does the project do?
- Accepts employee data uploaded by HR managers as a CSV file
- Runs each employee through an ML model to predict their attrition risk
- Stores the results in a PostgreSQL database per user account
- Displays interactive analytics dashboards: attrition rate, department breakdown, risk distribution
- Allows filtering employees by department and risk level
- Exports enriched reports (with risk scores) as downloadable CSV files

### What problem does it solve?
Employee attrition is costly and often reactive. HR teams typically discover an employee is leaving only after they resign. This system gives **early warning signals** by scoring every employee's risk of leaving, enabling HR to take proactive retention actions.

### Who are the target users?
- HR Managers and HR Business Partners
- People Analytics teams
- Small to mid-sized companies without dedicated ML/data science teams

### Why is this useful in the real world?
- **Cost savings**: Reducing turnover saves companies significant recruitment and onboarding costs
- **Proactive retention**: Identify high-risk employees before they leave
- **Data-driven HR**: Moves HR decision-making from gut feeling to evidence-based
- **Self-serve analytics**: HR teams don't need to depend on data scientists for every analysis

### Full Workflow (Input → Output)
```
User signs up / logs in
        ↓
Uploads CSV with employee data
        ↓
Backend validates columns
        ↓
Each employee row → ML model → risk_score + risk_level
        ↓
Data stored in PostgreSQL (linked to user_id)
        ↓
Frontend fetches analytics via REST APIs
        ↓
Dashboard renders charts, KPIs, employee table
        ↓
User can filter, explore, and export report CSV
```

### Architecture (Step-by-Step)
1. **React Frontend** makes HTTP requests to the Flask API
2. **JWT Token** is sent in headers for all protected routes
3. **Flask Backend** receives CSV → validates → calls predictor for each row
4. **Random Forest Model** (loaded from `.pkl` file via joblib) returns risk score
5. **PostgreSQL** stores enriched employee records under the user's account
6. **Analysis endpoints** query the DB, run pandas aggregations, return JSON
7. **Frontend** renders charts and tables from API responses

---

## 3. TECHNICAL BREAKDOWN

### Frontend
- **React (Vite)** — Fast SPA development with hot module replacement
- **React Context API** — Global auth state management (token, user info)
- **Axios** — HTTP client for API calls with base URL configuration
- **React Router** — Client-side routing between pages (Login, Dashboard, Upload, etc.)
- **Recharts / Chart library** — For bar charts, pie charts on the dashboard

### Backend
- **Flask** — Lightweight Python web framework, ideal for REST APIs
- **Flask Blueprints** — Modular routing: `auth`, `upload`, `analysis`, `reports`
- **Flask-JWT-Extended** — JWT creation and validation for protected routes
- **Flask-CORS** — Cross-origin resource sharing for React ↔ Flask communication
- **Pandas** — Data manipulation: reading CSVs, groupby aggregations for analytics
- **bcrypt** — Secure password hashing (never stored in plaintext)

### Database
- **PostgreSQL** — Relational database for structured employee data
- **psycopg2** — Python PostgreSQL driver for raw SQL queries
- **Two main tables**: `users` (id, name, email, password_hash) and `employees` (all columns + user_id FK, risk_score, risk_level)

### ML / AI
- **scikit-learn RandomForestClassifier** — 100 trees, random_state=42
- **Training data**: IBM HR Analytics dataset (1,470 employees, publicly available)
- **joblib** — Model serialization to `.pkl` file, loaded at prediction time
- **predict_proba** — Returns probability of attrition (class=1), multiplied by 100 = risk score

### Authentication
- **bcrypt** — Password hashing with salt on signup
- **JWT (JSON Web Tokens)** — Issued on login, stored in browser, sent in Authorization header
- **Per-user data isolation** — All employee queries filter by `user_id` from JWT identity

### Deployment *(Local/Development)*
- Backend: Flask dev server via `run.py` inside a Python virtual environment
- Frontend: Vite dev server via `npm run dev`
- Environment variables: managed via `.env` file with `python-dotenv`

---

## 4. APIs USED IN THE PROJECT

> **Note**: This project uses **internally built REST APIs** — no external third-party APIs.

### Internal REST API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/auth/signup` | POST | Register new user |
| `/api/auth/login` | POST | Login, returns JWT |
| `/api/upload/csv` | POST | Upload employee CSV |
| `/api/analysis/overview` | GET | Dashboard KPIs + risk distribution |
| `/api/analysis/department` | GET | Department-wise attrition breakdown |
| `/api/analysis/employees` | GET | Employee list with filters |
| `/api/analysis/factors` | GET | ML feature importance rankings |
| `/api/reports/export` | GET | Download enriched CSV report |

### What data is sent/received?
- **Upload**: Sends multipart/form-data (CSV file), receives `{message, count}`
- **Login**: Sends `{email, password}`, receives `{token, name, email}`
- **Overview**: Receives `{total_employees, attrition_rate, avg_age, avg_income, risk_distribution}`
- **Department**: Receives array of `{department, total_employees, attrition_count, attrition_rate, avg_risk_score}`

### Security
- All analysis/upload/report endpoints are protected with `@jwt_required()` decorator
- User data is isolated by `user_id` extracted from the JWT — one user cannot access another's data

### What if an API fails?
- All routes are wrapped in `try/except` blocks
- Returns `{error: "message"}` with appropriate HTTP status codes (400, 401, 404, 500)
- Frontend should display error messages to the user (graceful degradation)

---

## 5. ML / AI MODEL

### Model Used: **Random Forest Classifier**
- Library: `scikit-learn`
- Configuration: `n_estimators=100, random_state=42`

### Why Random Forest?
- Handles mixed data types (numerical + encoded categorical) well
- Naturally resistant to overfitting due to ensemble averaging
- Provides **feature importance** scores — very useful for explaining *why* an employee is high risk
- No need for feature scaling (unlike SVM or Logistic Regression)
- Fast inference — prediction per employee takes milliseconds

### Training Data
- **Dataset**: IBM HR Analytics Employee Attrition & Performance (Kaggle/IBM)
- **Size**: 1,470 employee records
- **Target**: `Attrition` column (Yes/No → 1/0)
- **Train/Test split**: 80% train, 20% test

### Features Used (12 features)
| Feature | Type |
|---|---|
| Age | Numerical |
| DistanceFromHome | Numerical |
| MonthlyIncome | Numerical |
| NumCompaniesWorked | Numerical |
| YearsAtCompany | Numerical |
| YearsSinceLastPromotion | Numerical |
| JobSatisfaction | Ordinal (1–4) |
| WorkLifeBalance | Ordinal (1–3) |
| EnvironmentSatisfaction | Ordinal (1–4) |
| OverTime_Yes | Binary encoded |
| Department_Research & Development | Binary encoded |
| Department_Sales | Binary encoded |

### How the Model Works at Inference
1. Employee row from CSV is passed as a Python dict
2. Categorical columns (OverTime, Department) are one-hot encoded
3. Missing features default to 0
4. `model.predict_proba(df)[0][1]` returns probability of attrition
5. Multiplied by 100 → risk_score (0–100)
6. Bucketed: ≥60 = High, 30–59 = Medium, <30 = Low

### Evaluation Metrics
- **Accuracy**: ~86% on test set (IBM dataset is imbalanced — ~16% attrition rate)
- **Classification Report**: Precision, Recall, F1 for both classes
- **Feature Importances**: MonthlyIncome, Age, YearsAtCompany typically top the list

### Possible Interview Questions on the Model

**Q: Why not use a neural network?**
> *"For tabular HR data of this size — around 1,470 records — a neural network would likely overfit and wouldn't give me feature importance, which is critical for HR interpretability. Random Forest is well-suited here."*

**Q: How did you handle class imbalance?**
> *"The IBM dataset has about 16% attrition cases, so it's imbalanced. For this project, I relied on Random Forest's inherent robustness. In production, I'd consider SMOTE oversampling or adjusting class_weight parameter."*

**Q: How do you know the model is accurate?**
> *"I printed accuracy score and a full classification report during training. The model achieves around 86% accuracy on the held-out test set, which is reasonable for this dataset."*

**Q: What is predict_proba?**
> *"predict_proba returns the probability for each class. Since it's binary classification — attrition Yes or No — I take index [1], which is the probability of the employee leaving, and multiply by 100 to get a human-readable risk score."*

---

## 6. CHALLENGES FACED

### Challenge 1: Class Imbalance in Training Data
- **Issue**: IBM dataset has ~84% non-attrition, ~16% attrition — model can be biased toward predicting "No"
- **Why**: Real-world attrition rates are naturally low
- **Solution**: Evaluated with full classification report (precision, recall, F1) rather than just accuracy. Accepted the trade-off for this version.
- **Learned**: Accuracy alone is a misleading metric for imbalanced datasets

### Challenge 2: CSV Column Validation
- **Issue**: Users might upload CSVs with different column names or missing columns
- **Why**: No standardized HR data format exists
- **Solution**: Added a strict `required_columns` check in the upload route that returns a clear error listing exactly which columns are missing
- **Learned**: Always validate data at the entry point with clear error messages

### Challenge 3: JWT Authentication Flow
- **Issue**: After login, protected routes were returning 401 even with a valid token
- **Why**: The `Authorization: Bearer <token>` header wasn't being sent correctly from the frontend
- **Solution**: Configured Axios with a request interceptor that automatically attaches the token from localStorage to every request
- **Learned**: Centralize auth header logic in one place rather than adding it to every API call

### Challenge 4: Per-User Data Isolation
- **Issue**: If multiple users upload data, they shouldn't see each other's employees
- **Why**: The `employees` table is shared
- **Solution**: Every DB query filters by `user_id` extracted from JWT. On new upload, the old employee records for that user are deleted first (`DELETE FROM employees WHERE user_id = %s`)
- **Learned**: Always design multi-tenant data isolation from day one

### Challenge 5: Model Loading on Every Prediction
- **Issue**: The model is loaded from disk (`.pkl`) on every single prediction call, which is slow for large CSVs
- **Why**: `load_model()` is called inside `predict_attrition()` for each row
- **Solution**: For this scale it works acceptably. In production, I'd load the model once at app startup and cache it in memory
- **Learned**: Lazy loading vs. eager loading trade-offs in ML serving

### Challenge 6: CORS Issues
- **Issue**: React frontend (localhost:5173) couldn't reach Flask backend (localhost:5000)
- **Why**: Browser blocks cross-origin requests by default
- **Solution**: Added `flask-cors` and called `CORS(app)` in the app factory
- **Learned**: CORS must be configured on the server side, not the client side

### Challenge 7: One-Hot Encoding Mismatch
- **Issue**: The ML model was trained with specific column names for one-hot encoded features. At inference time, the column names had to match exactly.
- **Why**: scikit-learn models expect the exact same feature schema at inference as at training
- **Solution**: Manually created `OverTime_Yes`, `Department_Research & Development`, `Department_Sales` columns in the predictor and explicitly selected only the `FEATURES` list
- **Learned**: Feature engineering at training and inference must be identical

---

## 7. INTERVIEW QUESTIONS AND ANSWERS

### Basic Questions

**Q: What is this project about?**
> *"It's an HR Attrition Analysis tool. HR managers upload employee data, and the system uses a Machine Learning model to predict which employees are at risk of leaving. It shows the results on an analytics dashboard with charts and filtering."*

**Q: Why did you build this project?**
> *"I wanted to build something that solves a real business problem and combines multiple technologies — full-stack web development, REST APIs, database design, and machine learning — all in one project. HR attrition is a well-understood domain with good public datasets, which made it great for learning."*

**Q: What is attrition?**
> *"Attrition refers to employees voluntarily leaving a company — resigning, retiring, or not renewing contracts. High attrition is expensive and disrupts business operations."*

---

### Intermediate Technical Questions

**Q: How does the CSV upload work end-to-end?**
> *"The user selects a CSV file on the frontend. React sends it as a multipart/form-data POST request with the JWT token in the header. Flask reads the file with pandas, validates that all required columns exist, then iterates over each row, runs the ML predictor to get a risk score, and inserts the result into PostgreSQL. At the end it returns a success message with the count of employees processed."*

**Q: How do you secure the API endpoints?**
> *"Every endpoint except signup and login is decorated with @jwt_required(). The user must include a valid JWT in the Authorization header. The JWT identity contains the user's ID, which is used to query only that user's data. Passwords are hashed with bcrypt before storage."*

**Q: Why did you use Flask instead of Django?**
> *"Flask is lightweight and gives me full control over the structure. For a REST API of this size, Django's ORM and admin interface would be overkill. Flask Blueprints gave me clean modularity without the overhead."*

**Q: Why PostgreSQL instead of MongoDB?**
> *"Employee data is inherently relational and structured. The relationship between users and their employees is a classic foreign key relationship. PostgreSQL gives me ACID compliance, strong typing, and efficient filtered queries — which is exactly what I need."*

**Q: How does the frontend manage authentication state?**
> *"I used React Context API to create an AuthContext that holds the JWT token and user info. On login, the token is stored in localStorage and set in the context. A custom useAuth hook exposes login, logout, and the current user. Protected routes check the context before rendering."*

---

### Advanced Architecture Questions

**Q: How would you scale this to 100,000 employees?**
> *"A few things would need to change: First, instead of iterating rows one by one in Python, I'd use pandas vectorized operations or batch predictions. Second, I'd cache the loaded ML model in memory at app startup rather than reading the .pkl file per prediction. Third, I'd add database indexes on user_id and department columns. For very large scale, I'd move the prediction step to a background job queue like Celery."*

**Q: Is this system multi-tenant?**
> *"Yes. Every employee record has a user_id foreign key. All queries filter by the user_id extracted from the JWT. One user's data is completely invisible to another user."*

**Q: What happens if a user uploads data twice?**
> *"The upload route first runs DELETE FROM employees WHERE user_id = %s before inserting the new records. So the previous dataset is replaced. This is a simple but effective approach. In a production system, I might version the uploads instead."*

**Q: How did you structure the Flask backend?**
> *"I used the Application Factory pattern with Flask Blueprints. The create_app() function initializes extensions like CORS, JWT, and registers four blueprints — auth, upload, analysis, and reports — each with its own URL prefix. This keeps the code modular and testable."*

---

### ML Questions

**Q: Why Random Forest for this problem?**
> *"Random Forest works well for tabular data, handles mixed feature types, doesn't require scaling, and provides feature importance — which is critical for HR use cases where you need to explain why an employee is flagged as high risk. It also generalizes well with relatively small datasets like the IBM HR dataset."*

**Q: What features does the model use?**
> *"12 features: Age, DistanceFromHome, MonthlyIncome, NumCompaniesWorked, YearsAtCompany, YearsSinceLastPromotion, JobSatisfaction, WorkLifeBalance, EnvironmentSatisfaction, and three binary-encoded features for OverTime, and two Department categories."*

**Q: What is predict_proba and why use it over predict?**
> *"predict() gives a binary 0 or 1 — leave or stay. predict_proba() gives the actual probability for each class. I use the probability of the positive class (attrition=1) to compute a continuous risk score from 0 to 100. This is much more useful for HR — they want to know how risky an employee is, not just a yes/no."*

**Q: How accurate is the model?**
> *"Around 86% accuracy on the test set. But I also look at the full classification report because the dataset is imbalanced — only about 16% of employees actually leave. A model that predicts 'No' for everyone would get 84% accuracy but be completely useless, so precision and recall for the attrition class matter more."*

---

### Database Questions

**Q: What does the employees table look like?**
> *"It has columns for: employee_number, age, department, job_role, monthly_income, years_at_company, years_since_last_promotion, overtime, job_satisfaction, attrition (Yes/No from the original CSV), risk_score (0–100 from ML), risk_level (High/Medium/Low), and user_id as a foreign key to the users table."*

**Q: How do you prevent SQL injection?**
> *"I use parameterized queries with psycopg2 — passing values as the second argument tuple to cur.execute() rather than string interpolation. psycopg2 handles escaping automatically."*

---

### HR / Ownership Questions

**Q: What did you personally build in this project?**
> *"I built everything end-to-end: the database schema, the ML model training script, the Flask REST API with all four blueprints, the React frontend with all pages and components, the authentication system, and the analytics logic. This was a solo project."*

**Q: What would you do differently if you built this again?**
> *"I'd load the ML model once at startup rather than per-prediction, add database connection pooling instead of opening a new connection per request, implement SMOTE to handle class imbalance better, and add proper unit tests from the start."*

---

## 8. PROJECT STRENGTHS

### What makes this project impressive?
- **End-to-end ownership**: Covers ML, backend, frontend, auth, database — shows full-stack maturity
- **Real ML integration**: Not just a CRUD app — actual trained model with probability outputs
- **Business relevance**: Attrition prediction is a genuine enterprise problem worth millions
- **Clean architecture**: Blueprints, services separation, JWT auth — production-grade patterns
- **Multi-tenant design**: Data isolation done right from day one
- **Feature importance endpoint**: Shows ability to make ML explainable, not just a black box

### What to highlight in an interview
- The fact that you trained your own model on a real dataset (IBM HR Analytics)
- The use of `predict_proba` for continuous risk scoring rather than binary classification
- Per-user data isolation as a real security consideration
- The export functionality — closes the loop from upload → analysis → actionable report

---

## 9. WEAKNESSES AND LIMITATIONS

### Honest Limitations
| Limitation | How to say it professionally |
|---|---|
| Model loaded from disk per prediction | *"In the current version, the model is loaded on each call. In production, I'd implement in-memory caching at startup."* |
| No connection pooling | *"I open a new DB connection per request. For production, I'd use SQLAlchemy with a connection pool."* |
| No SMOTE for class imbalance | *"The model handles imbalance reasonably, but I'd apply SMOTE in a production version for better recall on attrition cases."* |
| No model retraining pipeline | *"Currently the model is pre-trained. A production system would have a retraining pipeline as new data comes in."* |
| Deployed only locally | *"The current version runs locally. Deployment to a cloud platform like Render, Railway, or AWS is the next step."* |
| No email verification | *"Signup doesn't verify email — in production I'd add email verification."* |

### Future Improvements
- Model retraining on user's own uploaded data over time
- Employee-level drill-down pages with retention recommendations
- Email alerts when high-risk employees are detected
- Role-based access control (admin vs. viewer)
- Cloud deployment (Render/Railway for backend, Vercel for frontend)
- Unit and integration tests

---

## 10. RESUME AND INTERVIEW POSITIONING

### Primary Resume Bullet
> **Built an end-to-end HR Attrition Prediction System** using React, Flask, PostgreSQL, and scikit-learn; trained a Random Forest model on the IBM HR Analytics dataset to predict employee attrition with ~86% accuracy, delivering a risk-scored dashboard with department analytics, employee filtering, and CSV report export.

### Three Variations

**Variation 1 (ML-focused):**
> Designed and trained a Random Forest classifier on 1,470 employee records to predict HR attrition risk; integrated model into a Flask REST API with JWT authentication, serving real-time risk scores (0–100) to a React analytics dashboard.

**Variation 2 (Full-stack focused):**
> Developed a full-stack HR analytics web application with React frontend, Flask backend (4 REST API modules), PostgreSQL database, and an ML-powered attrition risk engine; implemented JWT auth, per-user data isolation, and CSV report generation.

**Variation 3 (Impact-focused):**
> Built a proactive HR attrition detection tool enabling HR teams to identify high-risk employees before they resign, using a Random Forest model achieving 86% accuracy on the IBM HR dataset; deployed as a full-stack web app with interactive dashboards and departmental analytics.

---

### LinkedIn Project Description
> **HR Attrition Analysis & Prediction System**
>
> A full-stack web application that empowers HR teams to predict and prevent employee attrition. HR managers upload employee data via CSV, and the system automatically scores every employee's risk of leaving using a Machine Learning model trained on the IBM HR Analytics dataset.
>
> 🔧 **Tech Stack**: React · Flask · PostgreSQL · scikit-learn · JWT Auth · pandas
>
> 🤖 **ML Model**: Random Forest Classifier (~86% accuracy) with continuous risk scoring (0–100) and feature importance analysis
>
> 📊 **Features**: Attrition dashboard · Department analysis · Risk distribution · Employee explorer with filtering · Enriched CSV report export
>
> This project combines full-stack engineering with practical ML deployment — covering everything from model training to REST API design to interactive data visualization.

---

### GitHub Project Description (README intro)
> **HR Attrition Analysis & Prediction System**
>
> A production-grade full-stack web application for HR attrition analysis and employee risk prediction.
>
> Upload your employee CSV → get instant ML-powered risk scores → explore department analytics → export enriched reports.
>
> **Stack**: React (Vite) · Flask · PostgreSQL · scikit-learn (Random Forest) · JWT Auth · bcrypt · pandas
>
> **Model**: Trained on IBM HR Analytics dataset · ~86% accuracy · predict_proba for continuous risk scoring · feature importance endpoint

---

## 11. FINAL SPEAKING SCRIPTS

### "Tell me about your project"
> *"I built an HR Attrition Analysis and Prediction System. It's a full-stack web app where HR managers can log in, upload a CSV of employee data, and instantly see which employees are at risk of leaving the company — powered by a Machine Learning model I trained.*
>
> *The backend is Flask with four REST API modules — auth, upload, analysis, and reports. The frontend is React. The database is PostgreSQL. And the ML model is a Random Forest classifier trained on the IBM HR Analytics dataset.*
>
> *When a CSV is uploaded, the system runs every employee row through the model, which gives back a risk score from 0 to 100. High risk is above 60, medium is 30 to 60, low is below 30. That data is saved to the database, and the dashboard immediately shows attrition rates by department, the risk distribution across the workforce, and a filterable employee table. There's also a report export feature."*

---

### "How does your project work?"
> *"At a high level: the user logs in and gets a JWT token. They upload a CSV file, which goes to a Flask endpoint. The backend validates that all required columns are present, then for each employee row, it calls the ML predictor — a Random Forest model loaded from a .pkl file — which returns a risk score and risk level.*
>
> *All of this is saved to PostgreSQL under the user's account. Then the frontend calls separate analysis endpoints to get overview stats, department breakdowns, and risk distributions. These endpoints query the database and use pandas for aggregations. The frontend renders everything as charts and tables.*
>
> *Every API call except login and signup requires a valid JWT. And all database queries filter by user_id from the token, so data is fully isolated between users."*

---

### "What challenges did you face?"
> *"A few key challenges. First, the feature engineering at inference time had to exactly match what I did during training. The model was trained with one-hot encoded columns for OverTime and Department. If those column names didn't match exactly at prediction time, the model would silently give wrong results. I solved that by explicitly defining the feature list and manually creating those columns in the predictor.*
>
> *Second, JWT authentication had a subtle bug — the frontend wasn't attaching the token correctly to requests. I fixed that by creating an Axios interceptor that automatically adds the Authorization header to every outgoing request.*
>
> *Third, the model loads from disk on every prediction call, which is inefficient. For this project it's acceptable, but I know in production I'd load the model once at app startup and keep it in memory."*

---

### "What APIs or models did you use?"
> *"For the ML model, I used a Random Forest Classifier from scikit-learn — 100 trees, trained on the IBM HR Analytics dataset with 1,470 records and 12 features. I serialize it with joblib and load it at inference time. The model outputs a probability of attrition using predict_proba, which I convert into a risk score from 0 to 100.*
>
> *For APIs, I didn't use any external third-party APIs. I built the entire REST API myself in Flask with four blueprints. The key endpoints are: auth for login and signup, upload for CSV ingestion, analysis for the dashboard data, and reports for CSV export. All protected endpoints require a JWT in the Authorization header."*

---

*Document generated by Antigravity based on full codebase analysis.*
*Project: hr-attrition-backend + hr-attrition-frontend*
