from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Enables frontend access
import os
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend (port 3000) to talk to backend (port 5000)

# ✅ Job roles & skills (2025-ready)
roles = {
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "Vue", "Angular", "Responsive Design"
    ],
    "Backend Developer": [
        "Python", "Java", "Node.js", "Django", "Flask", "Spring Boot", "API Development"
    ],
    "Full Stack Developer": [
        "JavaScript", "React", "Node.js", "Express", "MongoDB", "REST API", "Git"
    ],
    "Software Developer": [
        "OOP", "Git", "Algorithms", "Data Structures", "Design Patterns", "Unit Testing"
    ],
    "Data Analyst": [
        "Excel", "SQL", "Tableau", "Power BI", "Python", "Statistics", "Data Cleaning"
    ],
    "Data Scientist": [
        "Python", "Pandas", "NumPy", "Machine Learning", "Matplotlib", "Jupyter", "Statistics"
    ],
    "AI/ML Engineer": [
        "Python", "TensorFlow", "PyTorch", "Scikit-learn", "Deep Learning", "NLP", "Computer Vision"
    ],
    "DevOps Engineer": [
        "CI/CD", "Docker", "Kubernetes", "Jenkins", "Linux", "AWS", "Monitoring"
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "GCP", "Terraform", "CloudFormation", "Docker", "Serverless"
    ],
    "Cybersecurity Analyst": [
        "Network Security", "Firewalls", "Penetration Testing", "SIEM", "Encryption", "OWASP"
    ],
    "Mobile App Developer": [
        "Java", "Kotlin", "Swift", "Flutter", "React Native", "Android Studio", "iOS"
    ],
    "UI/UX Designer": [
        "Figma", "Sketch", "Adobe XD", "Wireframes", "Prototyping", "User Research", "Design Systems"
    ]
}

# ✅ Home route for testing if live
@app.route('/', methods=['GET'])
def home():
    return "✅ Smart Resume Analyzer Backend is LIVE!"

# ✅ Resume analyzer route
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # 🧠 Extract text from PDF
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text() or ""

    # 🔍 Match role percentages
    result = {}
    for role, skills in roles.items():
        match_count = sum(skill.lower() in resume_text.lower() for skill in skills)
        percentage = (match_count / len(skills)) * 100
        result[role] = round(percentage, 2)

    # 🏆 Best match
    best_role = max(result, key=result.get)
    best_percentage = result[best_role]

    return jsonify({
        "match_percentages": result,
        "best_match": {
            "role": best_role,
            "percentage": best_percentage
        }
    })

# ✅ Start server (Render-compatible)
if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


