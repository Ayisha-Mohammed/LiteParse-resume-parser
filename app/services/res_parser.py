
from werkzeug.datastructures import FileStorage
from app.utils.ext_text import extracted_text_from_pdf,extracted_text_from_docx
from app.utils.ext_data import extract_email,extract_phone,extract_name


def parse_resume(resume_file:FileStorage):
   #  print("Filename:", resume_file.filename)
   #  print("Content-Type:", resume_file.content_type)
    file_name= resume_file.filename.lower()
    if file_name.endswith('.pdf'):
       text = extracted_text_from_pdf(resume_file)
    elif file_name.endswith('.docx'):      
       text = extracted_text_from_docx(resume_file)
    else:
      return{"error":"Unsupported file format"}
   
    email=extract_email(text) 
    phone=extract_phone(text)
    name=extract_name(text)
    
   
    return {
      "Email":email,"phone":phone, "Name":name    }
   
   

       
    
