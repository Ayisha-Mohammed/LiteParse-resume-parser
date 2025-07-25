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
 education =[]
 deg_pattn = re.compile(r'\b(B\.?\s?(A|Sc|Com|Eng|Tech)|M\.?\s?(A|Sc|Com|Eng|Tech)|MBA|MCA|BCA|BBA|BE|ME|B\.?Tech|M\.?Tech|Ph\.?D|PhD|PGDM|Diploma|Certificate|Certification|Associate)\b'
 ,re.IGNORECASE)
 year_pattn = re.compile(r'(19|20)\d{2}[\s\-–]*(19|20)?\d{2}?'
 ,re.IGNORECASE)
 for line in text.spit():
    if deg_pattn.search(line):
       match_deg = deg_pattn.search(line)
       match_year=year_pattn.search(line)
    if match_deg:
       education.append({
          "degree": match_deg .group(),
          "year": match_year if match_year else None
       })
 return education


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
  
 