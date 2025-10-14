from flask import Blueprint, request, jsonify, current_app
from app.services.res_parser import parse_resume
from app.limiter import limiter
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


parser_bp = Blueprint("parser", __name__)
auth_bp = Blueprint("auth", __name__)


@jwt_required()
@parser_bp.route("/parse", methods=["POST"])
@limiter.limit("5 per minute")
def parse():
    try:
        resume_file = request.files.get("file")
        if not resume_file:
            return jsonify({"success": False, "error": "No resume uploaded"}), 400
        current_app.logger.info(f"Uploaded file: {resume_file.filename}")
        print("Uploaded Your file:", resume_file.filename)
        result_of_parsed_resume = parse_resume(resume_file)

        # Handle known errors returned from parser
        if isinstance(result_of_parsed_resume, dict) and result_of_parsed_resume.get(
            "error"
        ):
            return (
                jsonify({"success": False, "error": result_of_parsed_resume["error"]}),
                400,
            )

        return jsonify({"success": True, "data": result_of_parsed_resume}), 200

    except Exception as e:
        print("Unexpected error:", e)
        return (
            jsonify(
                {"success": False, "error": "Internal Server Error", "details": str(e)}
            ),
            500,
        )

    # Register new user


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    # Check if user exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(email=data["email"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "api_key": user.api_key}), 201


# Login user
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "api_key": user.api_key})
    return jsonify({"message": "Invalid credentials"}), 401


@parser_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"success": True, "message": "API is alive"}), 200
