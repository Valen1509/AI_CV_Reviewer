import os
import re
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import spacy

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_info(text):
    doc = nlp(text)

    # Email y Teléfono
    email_pattern = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_pattern = re.search(r"(\+?\d{1,2}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text)

    email = email_pattern.group(0) if email_pattern else "No encontrado"
    phone = phone_pattern.group(0) if phone_pattern else "No encontrado"

    # Nombre
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "No encontrado")

    # Habilidades
    skills_keywords = ['python', 'java', 'sql', 'excel', 'communication', 'teamwork',
                       'javascript', 'react', 'node.js', 'machine learning']
    found_skills = [kw for kw in skills_keywords if kw.lower() in text.lower()]

    # Educación
    education_keywords = ['Licenciatura', 'master', 'phd', 'engineering', 'degree', 'university', 'college']
    education = [line for line in text.split('\n') if any(keyword in line.lower() for keyword in education_keywords)]

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': list(set(found_skills)),
        'education': education[:2]  # máximo 2 líneas
    }

@app.route("/", methods=["GET", "POST"])
def index():
    resumes = []
    if request.method == "POST":
        files = request.files.getlist("files")
        for file in files:
            if file and file.filename.endswith(".pdf"):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                text = extract_text_from_pdf(file_path)
                info = extract_info(text)

                resumes.append({
                    'filename': file.filename,
                    'name': info['name'],
                    'email': info['email'],
                    'phone': info['phone'],
                    'skills': info['skills'],
                    'education': info['education'],
                    'score': len(info['skills'])
                })
    return render_template("index.html", resumes=resumes)

if __name__ == "__main__":
    app.run(debug=True)
