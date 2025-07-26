import spacy
import re
from spacy.matcher import PhraseMatcher
# from transformers import pipeline

nlp=spacy.load("en_core_web_sm")
# summarizer = pipeline("summarization", model= "sshleifer/distilbart-cnn-12-6") 

def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_phone(text):
    pattern = r'(\+?\d{1,3}[\s-]?)?\(?\d{3,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
    match = re.search(pattern, text)
    if match :
      return match.group()
    else:
       None

# def extract_name(text):
#    doc =nlp(text)~
#    for ent in doc.ents:
#       if ent.label_== "PERSON":
#        return ent.text
#    return None
def extract_name(resume_text):
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    lines = [line for line in lines if not re.fullmatch(r'[-=_~*\s]{3,}', line)]
    name_candidates = [
        line for line in lines[:10]
        if not re.search(r'[@]|https?://|www\.|linkedin|github|kaggle|\.com|\d', line, re.IGNORECASE)
        and 1 <= len(line.split()) <= 4
    ]

    for name in name_candidates:
        if name.isupper() or re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+$', name):
            return name.title()
    
    return name_candidates[0].title() if name_candidates else None
 
def extract_skills(text,Skills):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in Skills]
    matcher.add("SKILLS", patterns)
    doc = nlp(text)
    matches = matcher(doc)
    found_skills = {doc[start:end].text for _, start, end in matches}
    return list(found_skills)


def extract_education(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    degrees_found = []

    # Define start and end section markers
    start_pattern = re.compile(r'\bEducation\b', re.IGNORECASE)
    end_keywords = ['experience', 'project', 'certification', 'achievement', 'internship', 'skills', 'summary', 'work', 'profile']
    end_pattern = re.compile(r'^(' + '|'.join(end_keywords) + r')\b', re.IGNORECASE)

    # Degree pattern (ignore year)
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
    return {
        "degree": ', '.join(degrees_found)
    }


# def extract_education_section(text):
#     lines = text.split('\n')
#     edu_lines = []
#     capture = False
#     for line in lines:
#         lower = line.lower().strip()
#         if 'education' in lower:
#             capture = True
#             continue
#         elif capture and any(keyword in lower for keyword in ['experience', 'internship', 'project', 'summary', 'skills', 'certifications']):
#             break
#         if capture:
#             edu_lines.append(line)
#     return '\n'.join(edu_lines)


def extract_education_section(text):
    lines = text.split('\n')
    edu_lines = []
    capture = False
    for line in lines:
        lower = line.lower().strip()
        if 'education' in lower:
            capture = True
            continue
        elif capture and any(keyword in lower for keyword in ['experience', 'project', 'summary', 'skills', 'certifications']):
            break
        if capture:
            edu_lines.append(line.strip())
    return edu_lines



def extract_latest_degree_and_year(text):
    degree_priority = {
        'ph.d': 3, 'phd': 3, 'doctor of philosophy': 3,
        'm.tech': 2, 'mtech': 2, 'master of technology': 2,
        'm.sc': 2, 'msc': 2, 'master of science': 2,
        'mba': 2, 'master of business administration': 2,
        'mca': 2,
        'b.tech': 1, 'btech': 1, 'bachelor of technology': 1,
        'b.sc': 1, 'bsc': 1, 'bachelor of science': 1,
        'bca': 1,
        'bachelor of computer science': 1,
    }

    # Smart year range regex
    year_range_pattern = re.compile(r'(20\d{2}).*?(?:–|—|-|\sto\s).*?(20\d{2})', re.IGNORECASE)
    single_year_pattern = re.compile(r'(20\d{2})')

    edu_lines = extract_education_section(text)
    top_degree = ''
    top_year_range = ''
    top_rank = 0

    for i, line in enumerate(edu_lines):
        line_clean = re.sub(r'\s{2,}', ' ', line.strip().lower())  # collapse extra spaces

        for deg, rank in degree_priority.items():
            if re.search(r'\b' + re.escape(deg) + r'\b', line_clean):
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
                    year_range = single_year.group(1) if single_year else ''

                # Update if this degree has higher priority
                if rank > top_rank:
                    top_rank = rank
                    top_degree = deg.title()
                    top_year_range = year_range

    return {
        "degree": top_degree,
        "year": top_year_range
    }


def extract_edu_section(text):
    exp_sec_lines =[]
    lines=text.split("\n")
    capture= False
    for l in lines:
        lower=lines.strip().lower()
        if "experince" in  lower:
            capture = True
            continue
        elif any(keyword in lower for keyword in ["education","projects","certifications","skills"]):
            capture=False
        elif capture:
            exp_sec_lines.append(lines.strip())  
    return exp_sec_lines         
          




# def extract_latest_degree_and_year(text):
    degree_priority = {
        'ph.d': 3, 'phd': 3, 'doctor of philosophy': 3,
        'm.tech': 2, 'mtech': 2, 'master of technology': 2,
        'm.sc': 2, 'msc': 2, 'master of science': 2,
        'mba': 2, 'master of business administration': 2,
        'mca': 2,
        'b.tech': 1, 'btech': 1, 'bachelor of technology': 1,
        'b.sc': 1, 'bsc': 1, 'bachelor of science': 1,
        'bca': 1,
        'bachelor of computer science': 1,
    }

    # Smart year range regex
    year_range_pattern = re.compile(r'(20\d{2}).*?(?:–|—|-|\sto\s).*?(20\d{2})', re.IGNORECASE)
    single_year_pattern = re.compile(r'(20\d{2})')

    edu_lines = extract_education_section(text)
    top_degree = ''
    top_year_range = ''
    top_rank = 0

    for i, line in enumerate(edu_lines):
        line_clean = re.sub(r'\s{2,}', ' ', line.strip().lower())  # collapse extra spaces

        for deg, rank in degree_priority.items():
            if re.search(r'\b' + re.escape(deg) + r'\b', line_clean):
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
                    year_range = single_year.group(1) if single_year else ''

                # Update if this degree has higher priority
                if rank > top_rank:
                    top_rank = rank
                    top_degree = deg.title()
                    top_year_range = year_range

    return {
        "degree": top_degree,
        "year": top_year_range
    }

# def extract_latest_degree_and_year(text):
#     degree_priority = {
#         'ph.d': 3, 'phd': 3, 'doctor of philosophy': 3,
#         'm.tech': 2, 'mtech': 2, 'master of technology': 2,
#         'm.sc': 2, 'msc': 2, 'master of science': 2,
#         'mba': 2, 'master of business administration': 2,
#         'mca': 2,
#         'b.tech': 1, 'btech': 1, 'bachelor of technology': 1,
#         'b.sc': 1, 'bsc': 1, 'bachelor of science': 1,
#         'bca': 1,
#         'bachelor of computer science': 1,
#     }

#     edu_lines = extract_education_section(text)
#     top_degree = ''
#     top_year_range = ''
#     top_rank = 0

#     for i, line in enumerate(edu_lines):
#         line_clean = re.sub(r'\s{2,}', ' ', line.strip().lower())  # collapse spaces

#         for deg, rank in degree_priority.items():
#             if re.search(r'\b' + re.escape(deg) + r'\b', line_clean):
#                 # Check for year range in same line
#                 year_match = re.search(r'(20\d{2})\s*[-–—]\s*(20\d{2})', line_clean)

#                 # If not found, check next line
#                 if not year_match and i + 1 < len(edu_lines):
#                     next_line = edu_lines[i+1].lower()
#                     year_match = re.search(r'(20\d{2})\s*[-–—]\s*(20\d{2})', next_line)

#                 if year_match:
#                     year_range = f"{year_match.group(1)}–{year_match.group(2)}"
#                 else:
#                     # Check for single year fallback
#                     single_year = re.search(r'(20\d{2})', line_clean)
#                     if not single_year and i + 1 < len(edu_lines):
#                         single_year = re.search(r'(20\d{2})', edu_lines[i+1])
#                     year_range = single_year.group(1) if single_year else ''

#                 if rank > top_rank:
#                     top_rank = rank
#                     top_degree = deg.title()
#                     top_year_range = year_range

#     return {
#         "degree": top_degree,
#         "year": top_year_range
#     }

# def extract_latest_degree_and_year(text):
#     degree_priority = {
#         'ph.d': 3, 'phd': 3, 'doctor of philosophy': 3,
#         'm.tech': 2, 'mtech': 2, 'master of technology': 2,
#         'm.sc': 2, 'msc': 2, 'master of science': 2,
#         'mba': 2, 'master of business administration': 2,
#         'mca': 2,
#         'b.tech': 1, 'btech': 1, 'bachelor of technology': 1,
#         'b.sc': 1, 'bsc': 1, 'bachelor of science': 1,
#         'bca': 1,
#         'bachelor of computer science': 1,
#     }

#     edu_lines = extract_education_section(text)
#     top_degree = ''
#     top_year = ''
#     top_rank = 0

#     for i, line in enumerate(edu_lines):
#         line_clean = re.sub(r'\s{2,}', ' ', line.strip().lower())  # reduce multiple spaces

#         for deg, rank in degree_priority.items():
#             if re.search(r'\b' + re.escape(deg) + r'\b', line_clean):
#                 # Try to find year on same line
#                 year_match = re.search(r'(20\d{2})(?:[-–](\d{2,4}))?', line_clean)
                
#                 # If not found, check next line (if available)
#                 if not year_match and i + 1 < len(edu_lines):
#                     next_line = edu_lines[i+1].lower()
#                     year_match = re.search(r'(20\d{2})(?:[-–](\d{2,4}))?', next_line)

#                 year = ''
#                 if year_match:
#                     year = year_match.group(2) if year_match.group(2) else year_match.group(1)

#                     # if only last two digits, prefix current century
#                     if len(year) == 2:
#                         year = '20' + year

#                 if rank > top_rank:
#                     top_rank = rank
#                     top_degree = deg.title()
#                     top_year = year

#     return {
#         "degree": top_degree,
#         "year": top_year
#     }


# def extract_latest_degree_and_year(text):
#     degree_priority = {
#         'ph.d': 3, 'phd': 3, 'doctor of philosophy': 3,
#         'm.tech': 2, 'mtech': 2, 'master of technology': 2,
#         'm.sc': 2, 'msc': 2, 'master of science': 2,
#         'mba': 2, 'master of business administration': 2,
#         'mca': 2,
#         'b.tech': 1, 'btech': 1, 'bachelor of technology': 1,
#         'b.sc': 1, 'bsc': 1, 'bachelor of science': 1,
#         'bca': 1,
#         'bachelor of computer science': 1,
#     }

#     edu_text = extract_education_section(text)
#     lines = [line.lower().strip() for line in edu_text.split('\n') if line.strip()]

#     top_degree = ''
#     top_year = ''
#     top_rank = 0

#     for line in lines:
#         # Extract year (could be range like 2019–2021 or just one year)
#         year_match = re.search(r'20\d{2}(?:[-–]\d{2,4})?', line)
#         year = year_match.group(0)[-4:] if year_match else ''

#         # Split line by commas in case of multiple degrees
#         chunks = [chunk.strip() for chunk in line.split(',')]

#         for chunk in chunks:
#             for deg, rank in degree_priority.items():
#                 if re.search(r'\b' + re.escape(deg) + r'\b', chunk):
#                     if rank > top_rank:
#                         top_degree = chunk.title()
#                         top_year = year
#                         top_rank = rank

#     return {
#         "degree": top_degree,
#         "year": top_year
#     }




# # def extract_education(text):
# #  education =[]
# #  deg_pattn = re.compile(r'\b(B\.?\s?(A|Sc|Com|Eng|Tech)|M\.?\s?(A|Sc|Com|Eng|Tech)|MBA|MCA|BCA|BBA|BE|ME|B\.?Tech|M\.?Tech|Ph\.?D|PhD|PGDM|Diploma|Certificate|Certification|Associate)\b'
# #  ,re.IGNORECASE)
# #  year_pattn = re.compile(r'\b(19|20)\d{2}[\s\-]+\s*(19|20)?\d{2}?')
# #  for line in text.splitlines():
# #        print(line[:15])
# #        match_deg = re.search(deg_pattn,line)
# #        if match_deg:
# #         match_year=re.search(year_pattn,line)
# #         education.append({
# #           "degree": match_deg .group(),
#           "year": match_year.group() if match_year else None
#        })
#  return education


# def extract_summary(text):
#       keyword_re = re.compile(r'\b(experience|projects|developed|built|created|skilled|)\b', re.IGNORECASE)
#       lines = text.splitlines()
#       relevant_lines = [line.strip() for line in lines if keyword_re.search(line)]
#       result =" ".join(relevant_lines)

#       if len(result.split())<60:
#          return result
#       else:
#          summary = summarizer(result,max_length=100,min_length=50, do_sample=False)
#          return summary[0]["summary_text"]


#     # with open(text, "r", encoding="utf-8") as file:
#     #  raw_text= file.read()

# # T5 requires "summarize:" prefix
#     formatted_text = "summarize: " + text.strip()

# # Summarize
#     summary = summarizer(formatted_text, max_length=70, min_length=20, do_sample=False)
#     return summary[0]["summary_text"]
  
 