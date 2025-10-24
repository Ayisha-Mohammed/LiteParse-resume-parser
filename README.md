# LiteParse Resume Parser API

A lightweight API that extracts structured information from **PDF/DOCX resumes** — **name, email, phone number, education, skills, and basic project details**.  

Built with **Python, Flask, SQLAlchemy, and JWT authentication**, designed for HR tools, ATS systems, or resume-based applications.  

[ Live Demo](https://liteparse-resume-parser.onrender.com) | [GitHub Repo](https://github.com/yourusername/LiteParse-resume-parser)

---

## Features

- Python 3.13+  
- Flask REST API  
- Regex and keyword-based parsing  
- JWT authentication & API key support  
- PostgreSQL for user & API key management  
- JSON output for easy integration  

---

## Quick Start

No setup required for users — your API is **live on Render**:  

1. **Register a new account** → get your **API key**.  
2. **Login** → get your **JWT access token** (or continue using your API key).  
3. **Parse resumes** → upload PDF/DOCX files via `/parse` endpoint using Postman, curl, or your client.  

---

## API Endpoints

### Ping
Check if the API is live:

```http
GET /ping
Headers: Content-Type: application/json
Response:
{
  "success": true,
  "message": "API is alive"
}
```
### Register
```http
POST /register
Headers: Content-Type: application/json
Body:
{
  "email": "your_email",
  "password": "your_password"
}
Response:
{
  "message": "User created",
  "api_key": "generated_api_key_here"
}
```
### Login
```http
POST /login
Headers: Content-Type: application/json
Body:
{
  "email": "your_email",
  "password": "your_password"
}
Response:
{
  "access_token": "your_jwt_token_here",
  "api_key": "your_api_key_here"
}
```
### Parse
```http
POST /parse
Headers:
  Authorization: Bearer <JWT>
  or X-API-Key: <API_KEY>
Body:
  file: resume.pdf or resume.docx
Response:
{
  "success": true,
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1 234 567 890",
    "education": [
      {
        "degree": "B.Sc. Computer Science",
        "institution": "ABC University",
        "year": "2023"
      }
    ],
    "skills": ["Python", "Flask", "SQL", "Regex"],
    "projects": [
      {
        "title": "Resume Parser API",
        "description": "A lightweight API to parse resumes into structured JSON"
      }
    ]
  }
}
```
Note: Parsing is rule-based, so results may not be 100% accurate, especially if resume formatting is unusual. Use output as a guideline.

Testing with Postman:

Ping: GET https://liteparse-resume-parser.onrender.com/ping
Register/Login: JSON body requests
Parse: Upload resume as form-data, include JWT or API key in headers

Security Notes:

Keep your API key and JWT tokens confidential.
Do not hardcode credentials in scripts or apps.
Rate-limiting is enabled to prevent abuse.

Developer Section :

For developers who want to run the API locally:

git clone https://github.com/yourusername/LiteParse-resume-parser.git
cd LiteParse-resume-parser
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
flask run
You’ll need to provide your own .env with DATABASE_URL and JWT_SECRET_KEY for local testing.
