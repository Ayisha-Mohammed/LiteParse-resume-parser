import textwrap
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ext_data import (
    extract_phone,
    extract_email,
    extract_name,
    extract_education,
    extract_latest_degree_and_year,
    extract_projects,
    extract_skills
)

# ------------------- Email Tests -------------------
def test_extract_email_valid():
    text = "Contact me at abc@example.com"
    assert extract_email(text) == "abc@example.com"

def test_extract_email_no_email():
    text = "No email in this text"
    assert extract_email(text) is None

def test_extract_email_multiple():
    text = "Emails: first@domain.com, second@domain.com"
    assert extract_email(text) == "first@domain.com"

def test_extract_email_invalid_format():
    text = "My email is abc.com or user@domain"
    assert extract_email(text) is None

def test_extract_email_empty_text():
    text = ""
    assert extract_email(text) is None

# ------------------- Phone Tests -------------------
def test_extract_phone_valid():
    text = "Call me at +1-123-456-7890"
    assert extract_phone(text) == "+1-123-456-7890"

def test_extract_phone_no_phone():
    text = "No phone here"
    assert extract_phone(text) is None

# ------------------- Name Tests -------------------
def test_extract_name_valid():
    text = "John Doe"
    assert extract_name(text) == "John Doe"

def test_extract_name_missing():
    text = ""
    assert extract_name(text) is None

# ------------------- Education Tests -------------------
def test_extract_education_valid():
    text = """
    Education
    B.Tech in Computer Science, 2020
    """
    assert extract_education(text) == {"degree": "B.Tech in Computer Science"}

def test_extract_education_empty():
    text = ""
    assert extract_education(text) == {"degree": ""}

def test_latest_degree_and_year_valid():
    text = """
    Education
    B.Tech in CS 2020
    M.Tech in AI 2022
    """
    result = extract_latest_degree_and_year(text)
    assert result == {"degree": "M.Tech", "year": "2022"}

# ------------------- Projects Tests -------------------
def test_projects_valid():
    text = textwrap.dedent("""
        Projects
        Resume Parser
        Chatbot
    """)
    projects = extract_projects(text)
    assert "Resume Parser" in projects

# ------------------- Skills Tests -------------------
def test_extract_skills_one():
    text = "I am proficient in Python."
    skills_list = ["Python", "Java", "SQL","AWS"]
    assert extract_skills(text,skills_list) == ["Python"]

def test_extract_skills_multiple():
    text = "I know Python, SQL, and AWS."
    skills_list = ["Python", "Java", "SQL","AWS"]
    assert set(extract_skills(text,skills_list)) == set(["Python", "SQL", "AWS"])

def test_extract_skills_none():
    text = "I like painting."
    skills_list = ["Python", "Java", "SQL","AWS"]
    assert extract_skills(text,skills_list) == []

def test_extract_skills_case_insensitive():
    text = "Experience with java and sql."
    skills_list = ["Python", "Java", "SQL","AWS"]
    extracted = extract_skills(text, skills_list)
    # Compare lowercase versions to ignore capitalization
    assert set(s.lower() for s in extracted) == set(["java", "sql"])
    
def test_extract_skills_empty_text():
    text = ""
    skills_list = ["Python", "Java", "SQL","AWS"]
    assert extract_skills(text,skills_list) == []
