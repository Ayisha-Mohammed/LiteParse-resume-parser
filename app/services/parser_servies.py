import re
import fitz
import docx
from werkzeug.datastructures import FileStorage

def extracted_text_from_pdf(resume_file):
   text=''
   with fitz.open(stream=resume_file.read(),filetype="pdf")as doc :
    for page in doc:
       text += page.get_text()
   return text

def extracted_text_from_docx(resume_file):
    doc = docx.Document(resume_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume(resume_file:FileStorage):
    file_name= resume_file.filename.lower()
    if file_name.endswith('.pdf'):
       extracted_pdftext = extracted_text_from_pdf(resume_file)
    if file_name.endswith('.docx'):
       extracted_doctext = extracted_text_from_docx(resume_file)
    else:
      return{"error":"Unsupported file format"}
    
    return {"raw text:",  extracted_pdftext}

    