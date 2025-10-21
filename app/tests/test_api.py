# app/tests/test_api.py
import io
import pytest
from docx import Document
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import User
import uuid
from conftest import full_resume  # your text fixtures


# -------------------- Client Fixture --------------------
@pytest.fixture
def client():
    """Flask test client with JWT auth set up."""
    app = create_app()

    # Override config for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create test user
        test_user = User(
            username="testuser",
            email="test@example.com",
            password="hashedpw",
            api_key=str(uuid.uuid4()),
        )
        db.session.add(test_user)
        db.session.commit()

        # Create JWT token
        access_token = create_access_token(identity=str(test_user.id))

    # Create test client and attach token to each request
    client = app.test_client()
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
    return client


# -------------------- Helper --------------------
def make_docx_file(text: str) -> io.BytesIO:
    """Create in-memory .docx file from text."""
    buffer = io.BytesIO()
    doc = Document()
    doc.add_paragraph(text)
    doc.save(buffer)
    buffer.seek(0)
    return buffer


# -------------------- Health Check --------------------
def test_health_check(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json == {"success": True, "message": "API is alive"}


# -------------------- Parse Resume Tests --------------------
def test_parse_resume_full(client, full_resume):
    fake_file = make_docx_file(full_resume)
    data = {"resume": (fake_file, "resume.docx")}
    response = client.post(
        "/parse",
        data=data,
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
        follow_redirects=False,  # ensure no redirect
    )

    print(response.data)  # debug: see what the server actually returned

    assert response.status_code == 200
    assert response.is_json  # first check that response is JSON
    assert response.json["success"] is True


# def test_parse_resume_tricky(client, tricky_resume):
#     """Test POST /parse endpoint with tricky formatting resume."""
#     fake_file = make_docx_file(tricky_resume)
#     data = {"resume": (fake_file, "tricky_resume.docx")}

#     response = client.post(
#         "/parse",
#         data=data,
#         content_type="multipart/form-data",
#         follow_redirects=False,  # don't follow redirects
#     )

#     print("\nTRICKY RESUME RESPONSE:", response.data)

#     # Ensure valid response type
#     assert response.status_code == 200, response.data
#     assert response.is_json, f"Non-JSON response: {response.data}"
#     assert response.json["success"] is True
