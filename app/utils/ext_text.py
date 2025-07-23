
import fitz
import docx

def extracted_text_from_pdf(resume_file):
   text=""
   with fitz.open(stream=resume_file.read(),filetype="pdf")as doc :
    for page in doc:
       text += page.get_text()
   return text

def extracted_text_from_docx(resume_file):
    doc = docx.Document(resume_file)
    text = ""
    for para in doc.paragraph:
       text+=para.text+"/n"
    return text

# def load_sklist(filepath):
#    with open(filepath, 'r' , encoding='utf-8') as f:
#       return[line.strip() for line in f if line.strip()]
   
 