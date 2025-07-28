#Resume Parser API

A lightweight API that extracts structured information from pdf /doc resume — iname, email, phone number, education, skills, and basic project details.
This project is built using Python and regex-based logic, designed for use in HR tools, ATS systems, or resume-based applications.

##Demo
[Live on RapidAPI](https://your-rapidapi-link.com) *(replace with your actual URL once deployed)*  
[GitHub Repository](https://github.com/yourusername/resume-parser-api)

> Note: This API uses rule-based parsing (regex and keyword matching), so accuracy may vary depending on the formatting and structure of resumes.

## 
- Python 3.x
- Regex (Pattern Matching)
- Flask 
- JSON , NLP

## API Endpoint
### `POST /parse`

Accepts a resume file and returns extracted information in JSON format.

#### Request

- **Method:** `POST`
- **URL:** `/parse`
- **Headers:** `Content-Type: multipart/form-data`
- **Body:**  
  - `file`: Resume file in `.pdf` or `.docx` format
 
curl -X POST http://localhost:5000/parse \
  -F "file=@/path/to/resume.pdf"


