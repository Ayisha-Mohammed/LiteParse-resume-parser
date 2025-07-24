import spacy
import re
from spacy.matcher import PhraseMatcher
from transformers import pipeline

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

nlp=spacy.load("en_core_web_sm")

def extract_name(text):
   doc =nlp(text)
   for ent in doc.ents:
      if ent.label_== "PERSON":
       return ent.text
      return None
   
def extract_skills(text,Skills):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in Skills]
    matcher.add("SKILLS", patterns)
    doc = nlp(text)
    matches = matcher(doc)
    found_skills = {doc[start:end].text for _, start, end in matches}
    return list(found_skills)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
def extract_summary(text):
    keyword_re = re.compile(r'\b(experience|project|developed|built|created)\b', re.IGNORECASE)
    lines = text.splitlines()
    relevant_lines = [line.strip() for line in lines if keyword_re.search(line)]
    result =" ".join(relevant_lines)

    if len(result.split())<50:
       return result
    else:
       summary = summarizer(result,max_length=50,min_length=20, do_sample=False)
       return summary[0]["summary_text"]
  
 