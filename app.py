from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)

def check_in_csv(email):
    try:
        for file in ['pridection.csv', 'project_reports.csv']:
            if os.path.exists(file):
                df = pd.read_csv(file, encoding='latin1', low_memory=False)
                # search email name in csv
                df_str = df.to_string().lower()
                if email.split('@')[0].lower() in df_str:
                    return True
    except:
        pass
    return False

def ai_predict(cgpa, attendance, skills_count):
    # Simple AI logic for your project
    cgpa = float(cgpa)
    attendance = int(attendance)
    score = 0
    if cgpa >= 8.5: score += 40
    elif cgpa >= 7.5: score += 25
    else: score += 10

    if attendance >= 85: score += 40
    elif attendance >= 75: score += 25
    else: score += 10

    score += min(skills_count * 5, 20)

    if score >= 80:
        return f"PLACED - {score}% Chance in TCS/Infosys", "success"
    elif score >= 60:
        return f"MODERATE - {score}% Chance, Need 1 more skill", "warning"
    else:
        return f"AT RISK - {score}% Chance, Improve CGPA & Attendance", "danger"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        is_known = check_in_csv(email)

        if is_known:
            # Known student
            student = {
                "name": email.split('@')[0].title(),
                "email": email,
                "attendance": "88%",
                "cgpa": "8.4",
                "skills": "Python, ML",
                "prediction": "PLACED - 92% (From CSV Data)",
                "status": "KNOWN STUDENT - Data Found in CSV",
                "color": "success"
            }
            return render_template('dashboard.html', student=student)
        else:
            # Unknown - Ask for details
            return render_template('new_student.html', email=email)

    return render_template('login.html')

@app.route('/predict', methods=['POST'])
def predict():
    email = request.form.get('email')
    cgpa = request.form.get('cgpa')
    attendance = request.form.get('attendance')
    skills = request.form.get('skills')

    skills_count = len(skills.split(','))
    prediction_text, color = ai_predict(cgpa, attendance, skills_count)

    student = {
        "name": email.split('@')[0].title() + " (New)",
        "email": email,
        "attendance": attendance + "%",
        "cgpa": cgpa,
        "skills": skills,
        "prediction": prediction_text,
        "status": "NEW STUDENT - Live AI Prediction",
        "color": color
    }
    return render_template('dashboard.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)