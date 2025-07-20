import re
import fitz
import docx
from werkzeug.datastructures import FileStorage
from utils.ext_text import extracted_text_from_pdf,extracted_text_from_docx
from utils.ext_data import extract_email,extract_phone
import jsonify


def parse_resume(resume_file:FileStorage):
    file_name= resume_file.filename.lower()
    if file_name.endswith('.pdf'):
       text = extracted_text_from_pdf(resume_file)
    if file_name.endswith('.docx'):      
       text = extracted_text_from_docx(resume_file)
    else:
      return{"error":"Unsupported file format"}
    
    email=extract_email(text) 
    phone=extract_phone(text)
   
    return {
      "Email":email,"phone":phone
    }
   
   

       
    
