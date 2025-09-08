#Resume Parser API

A lightweight API that extracts structured information from pdf /doc resume — iname, email, phone number, education, skills, and basic project details.
This project is built using Python and regex-based logic, designed for use in HR tools, ATS systems, or resume-based applications.

## 
- Python 3.x
- Regex (Pattern Matching)
- Flask 
- JSON , NLP
## USAGE
clone the repo . create a virtual env . install dependencies .run the servers

## API Endpoint
### `POST /parse`
### `GET /ping`
Accepts a resume file and returns extracted information in JSON format.


use postman:
URL:https://liteparse-resume-parser.onrender.com

GET /ping > headers : [key > Content-Type] [value > application/json] >send -------------- to check api alive .

POST /parse
Request
Method: POST
Endpoint: /parse
Content-Type: multipart/form-data
Body: key = file, value = uploaded .pdf or .docx file
-Example (using Postman):
Go to Body → form-data
Add a key called file, choose a file (.pdf or .docx)
send


> Note: This API uses rule-based parsing (regex and keyword matching), so accuracy may vary depending on the formatting and structure of resumes.Not 100% precise .

