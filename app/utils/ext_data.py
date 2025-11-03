# Dear dev , NO enough resources, no big models, no perfect accuracy
# Hope you can tho!!

import spacy
import re
from spacy.matcher import PhraseMatcher

# from transformers import pipeline ,transformers failed no resource !!

nlp = spacy.load("en_core_web_sm")
# summarizer = pipeline("summarization", model= "sshleifer/distilbart-cnn-12-6")


def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_phone(text):
    pattern = r"(\+?\d{1,3}[\s-]?)?\(?\d{3,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


def extract_name(resume_text):
    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    lines = [line for line in lines if not re.fullmatch(r"[-=_~*\s]{3,}", line)]
    name_candidates = [
        line
        for line in lines[:10]
        if not re.search(
            r"[@]|https?://|www\.|linkedin|github|kaggle|\.com|\d", line, re.IGNORECASE
        )
        and 1 <= len(line.split()) <= 4
    ]

    for name in name_candidates:
        if name.isupper() or re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+$", name):
            return name.title()

    return name_candidates[0].title() if name_candidates else None


def extract_skills(text, Skills):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in Skills]
    matcher.add("SKILLS", patterns)
    doc = nlp(text)
    matches = matcher(doc)
    found_skills = {doc[start:end].text for _, start, end in matches}
    return list(found_skills)


def extract_education(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    degrees_found = []

    # Define start and end section markers
    start_pattern = re.compile(r"\bEducation\b", re.IGNORECASE)
    end_keywords = [
        "experience",
        "project",
        "certification",
        "achievement",
        "internship",
        "skills",
        "summary",
        "work",
        "profile",
    ]
    end_pattern = re.compile(r"^(" + "|".join(end_keywords) + r")\b", re.IGNORECASE)

    # Degree pattern (im ignoring year here)
    degree_keywords = r"(Bachelor|Master|B\.?Tech|M\.?Tech|MBA|MCA|BCA|B\.?Sc|M\.?Sc|Ph\.?D|Diploma|12th|10th)"
    degree_pattern = re.compile(rf"({degree_keywords}[^,\n]*)", re.IGNORECASE)

    in_education = False

    for line in lines:
        lower_line = line.lower()
        # Start from Education
        if not in_education:
            if start_pattern.search(line):
                in_education = True
            continue
        # Stop at next section
        if end_pattern.search(lower_line):
            break
        # Extract degree only
        degree_match = degree_pattern.search(line)
        if degree_match:
            degree = degree_match.group(0).strip()
            degrees_found.append(degree)

    # Join degrees with comma
    return {"degree": ", ".join(degrees_found)}


def extract_education_section(text):
    lines = text.split("\n")
    edu_lines = []
    capture = False
    for line in lines:
        lower = line.lower().strip()
        if "education" in lower:
            capture = True
            continue
        elif capture and any(
            keyword in lower
            for keyword in [
                "experience",
                "project",
                "summary",
                "skills",
                "certifications",
            ]
        ):
            break
        if capture:
            edu_lines.append(line.strip())
    return edu_lines


def extract_latest_degree_and_year(text):
    degree_priority = {
        "ph.d": 3,
        "phd": 3,
        "doctor of philosophy": 3,
        "m.tech": 2,
        "mtech": 2,
        "master of technology": 2,
        "m.sc": 2,
        "msc": 2,
        "master of science": 2,
        "mba": 2,
        "master of business administration": 2,
        "mca": 2,
        "b.tech": 1,
        "btech": 1,
        "bachelor of technology": 1,
        "b.sc": 1,
        "bsc": 1,
        "bachelor of science": 1,
        "bca": 1,
        "bachelor of computer science": 1,
    }

    # year range regex
    year_range_pattern = re.compile(
        r"(20\d{2}).*?(?:–|—|-|\sto\s).*?(20\d{2})", re.IGNORECASE
    )
    single_year_pattern = re.compile(r"(20\d{2})")

    edu_lines = extract_education_section(text)
    top_degree = ""
    top_year_range = ""
    top_rank = 0

    for i, line in enumerate(edu_lines):
        line_clean = re.sub(
            r"\s{2,}", " ", line.strip().lower()
        )  # collapse extra spaces

        for deg, rank in degree_priority.items():
            if re.search(r"\b" + re.escape(deg) + r"\b", line_clean):
                # Look for year range in same line
                year_match = year_range_pattern.search(line_clean)

                # Check next line if not found
                if not year_match and i + 1 < len(edu_lines):
                    year_match = year_range_pattern.search(edu_lines[i + 1].lower())

                if year_match:
                    year_range = f"{year_match.group(1)}–{year_match.group(2)}"
                else:
                    # Try to find a single year as fallback
                    single_year = single_year_pattern.search(line_clean)
                    if not single_year and i + 1 < len(edu_lines):
                        single_year = single_year_pattern.search(edu_lines[i + 1])
                    year_range = single_year.group(1) if single_year else ""

                # Update if this degree has higher priority
                if rank > top_rank:
                    top_rank = rank
                    top_degree = deg.title()
                    top_year_range = year_range

    return {"degree": top_degree, "year": top_year_range}


def extract_projects(text):
    lines = text.split("\n")
    titles = []
    capture = False

    project_keywords = [
        "project",
        "projects",
        "academic project",
        "major project",
        "minor project",
        "report",
    ]
    other_sections = [
        "education",
        "skills",
        "certification",
        "experience",
        "internship",
        "contact",
        "summary",
        "profile",
        "personal",
    ]

    for line in lines:
        clean = line.strip()
        lower = clean.lower()

        # Step 1: Start capturing when line looks like a project section
        if not capture and any(kw in lower for kw in project_keywords):
            capture = True
            continue

        # Step 2: Stop capturing if line looks like a new section
        if capture and any(kw in lower for kw in other_sections):
            break

        # Step 3: If capturing, clean the line and add
        if capture and clean:
            # Remove bullets, dashes, numbers, etc.
            clean = re.sub(r"^[\-\*\▪\d\.\)\(]+\s*", "", clean)
            if 1 <= len(clean.split()) <= 15:  # allow slightly longer project names
                titles.append(clean)

    return titles


# def extract_projects(text):
#     lines = text.split('\n')
#     titles = []
#     capture = False
#     project_keywords = ['project', 'projects', 'academic project', 'major project'
# ,'minor project', 'report']
# 'internship','contact','summary','profile','personal']
#     for line in lines:
#         clean = line.strip()
#         lower = clean.lower()

#         # Step 1: Start capturing
#         if not capture and any(kw in lower for kw in project_keywords):
#             capture = True
#             continue

#         # Step 2: Stop at another section
#         if capture and any(kw in lower for kw in other_sections):
#             break

# Step 3: Only get clean, likely title lines (non-bullets, not too long, not too short)
# if capture and clean and not clean.startswith(('▪', '-', '*')) and 1<=
#  len(clean.split()) <= 10:
# titles.append(clean)
# return titles
