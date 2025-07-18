import re
import fitz
import docx
from werkzeug.datastructures import FileStorage

def extracted_text_from_pdf(resume_file):
   return

def extracted_text_from_docx(resume_file):
   return
   






def parse_resume(resume_file:FileStorage):
    file_name= resume_file.filename.lower()
    if file_name.endswith('.pdf'):
       extracted_pdftext = extracted_text_from_pdf(resume_file)
    if file_name.endswith('.docx'):
       extracted_doctext = extracted_text_from_docx(resume_file)
    else:
      return{"error":"Unsupported file format"}
    
    return {"raw text:",  extracted_pdftext}

    