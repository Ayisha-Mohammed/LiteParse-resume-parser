# tests/test_resume_pipeline.py

import sys
import os

# Make app imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.ext_data import (
    extract_phone,
    extract_email,
    extract_name,
    extract_education,
    extract_latest_degree_and_year,
    extract_projects,
    extract_skills,
)


# ---------------- FULL RESUME PIPELINE ----------------
def test_resume_pipeline_full(full_resume, skills_list):
    name = extract_name(full_resume)
    phone = extract_phone(full_resume)
    email = extract_email(full_resume)
    edu = extract_education(full_resume)
    latest_degree = extract_latest_degree_and_year(full_resume)
    skills = extract_skills(full_resume, skills_list)
    projects = extract_projects(full_resume)

    # ---------------- Assertions ----------------
    assert isinstance(name, str) and len(name) > 0
    assert phone == "+91 9876543210"
    assert email == "john.doe@example.com"
    assert isinstance(edu, dict) and "degree" in edu
    assert (
        isinstance(latest_degree, dict)
        and "degree" in latest_degree
        and "year" in latest_degree
    )
    assert set(s.lower() for s in skills) == set([s.lower() for s in skills_list])
    assert "Resume Parser" in projects
    assert "Chatbot" in projects


# ---------------- TRICKY FORMATTING ----------------
# def test_resume_pipeline_tricky_format(tricky_resume, skills_list):
#     name = extract_name(tricky_resume)
#     phone = extract_phone(tricky_resume)
#     email = extract_email(tricky_resume)
#     edu = extract_education(tricky_resume)
#     latest_degree = extract_latest_degree_and_year(tricky_resume)
#     skills = extract_skills(tricky_resume, skills_list)
#     projects = extract_projects(tricky_resume)

#     # ---------------- Assertions ----------------
#     assert isinstance(name, str) and len(name) > 0
#     assert phone == "9876543210"
#     assert email == "john.doe@example.com"
#     assert isinstance(edu, dict) and "degree" in edu
#     assert (
#         isinstance(latest_degree, dict)
#         and "degree" in latest_degree
#         and "year" in latest_degree
#     )
#     assert set(s.lower() for s in skills) == set([s.lower() for s in skills_list])
#     assert "Resume Parser" in projects
