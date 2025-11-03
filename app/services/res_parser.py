import os
from werkzeug.datastructures import FileStorage
from app.utils.ext_text import extracted_text_from_pdf, extracted_text_from_docx
from app.utils.ext_data import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills,
    extract_education,
    extract_latest_degree_and_year,
    extract_projects,
)


def parse_resume(resume_file: FileStorage):
    file_name = resume_file.filename.lower()
    if file_name.endswith(".pdf"):
        text = extracted_text_from_pdf(resume_file)
    elif file_name.endswith(".docx"):
        text = extracted_text_from_docx(resume_file)
    else:
        return {"error": "Unsupported file format"}

    # Load skills list ...can also implement using a DB(later)!!
    skills_path = os.path.join(os.path.dirname(__file__), "skill_list.txt")
    with open(skills_path, "r", encoding="utf-8") as f:
        Skills = [line.strip() for line in f if line.strip()]

    # Extractings
    email = extract_email(text) or ""
    phone = extract_phone(text) or ""
    name = extract_name(text) or ""
    skills = extract_skills(text, Skills) or []
    education = extract_education(text) or {"degree": ""}
    latest_deg = extract_latest_degree_and_year(text) or {"degree": "", "year": ""}
    projects = extract_projects(text) or []

    # Always return consistent dict
    return {
        "Email": email,
        "Phone": phone,
        "Name": name,
        "Skills": ", ".join(skills),
        "Education": education,
        "Latest degree": latest_deg,
        "Projects": projects,
    }
