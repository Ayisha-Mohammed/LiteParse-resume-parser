from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from app.services.res_parser import parse_resume
from app.limiter import limiter
from app import db, bcrypt
from app.models import User
from functools import wraps

# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)


parser_bp = Blueprint("parser", __name__)
auth_bp = Blueprint("auth", __name__)
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/docs")
def docs():
    return render_template("docs.html")

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # If Authorization header exists, use JWT
        auth_header = request.headers.get("Authorization", None)
        if auth_header and auth_header.startswith("Bearer "):
            try:
                verify_jwt_in_request()
                identity = get_jwt_identity()
                if not identity:
                    return jsonify({"success": False, "error": "JWT required"}), 401
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 401
        else:
            # Fallback to session-based auth
            if "user" not in session:
                flash("Please log in first.")
                return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return wrapper

# 1. Add this decorator (can also move to utils.py later)
# def auth_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if request.is_json:
#             verify_jwt_in_request()
#             identity = get_jwt_identity()
#             if not identity:
#                 return jsonify({"success": False, "error": "JWT required"}), 401
#         else:
#             if "user" not in session:
#                 flash("Please log in first.")
#                 return redirect(url_for("main.home"))
#         return f(*args, **kwargs)

#     return wrapper


@parser_bp.route("/parse", methods=["POST"])
# @jwt_required()
@auth_required
@limiter.limit("5 per minute")
def parse():
    try:
        resume_file = request.files.get("resume")
        if not resume_file:
            flash("No resume uploaded.")
            return redirect(url_for("main.home"))

        result_of_parsed_resume = parse_resume(resume_file)

        # Handle known parser errors
        if isinstance(result_of_parsed_resume, dict) and result_of_parsed_resume.get(
            "error"
        ):
            if request.is_json:
                return (
                    jsonify(
                        {"success": False, "error": result_of_parsed_resume["error"]}
                    ),
                    400,
                )
            flash(result_of_parsed_resume["error"])
            return redirect(url_for("main.home"))

        if request.is_json:
            return jsonify({"success": True, "data": result_of_parsed_resume}), 200

        # For browser: render result on the same home page
        return render_template(
            "home.html", parsed_data=result_of_parsed_resume, user=session.get("user")
        )

    except Exception as e:
        print("Unexpected error:", e)
        if request.is_json:
            return jsonify({"success": False, "error": str(e)}), 500
        flash("Something went wrong while parsing the resume.")
        return redirect(url_for("main.home"))

    # Register new user


@auth_bp.route("/register", methods=["POST"])
def register():
    # Determine request type
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    # Validate input
    if not email or not password or not username:
        if request.is_json:
            return jsonify({"message": "Email,password,username required"}), 400
        else:
            flash("Email,password,username required")
            return redirect(url_for("main.home"))  # your home.html

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        if request.is_json:
            return jsonify({"message": "User already exists"}), 400
        else:
            flash("User already exists")
            return redirect(url_for("main.home"))
    # Create user
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(
        username=username,
        email=email,
        password=hashed_password,
    )
    db.session.add(user)
    db.session.commit()
    # Log in user (optional)
    # session['user'] = {"id": user.id, "username": user.email}
    if request.is_json:
        return jsonify({"message": "User created", "api_key": user.api_key}), 201
    else:
        flash("Registration successful")
        return redirect(url_for("main.home"))


# Login user
@auth_bp.route("/login", methods=["POST"])
def login():
    email = password = None

    if request.is_json:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    # Input validation
    if not email or not password:
        if request.is_json:
            return jsonify({"message": "Email and password are required"}), 400
        else:
            flash("Email and password are required", "error")
            return redirect(url_for("main.home"))

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session["user"] = {"id": user.id, "username": user.username}
        if request.is_json:
            access_token = create_access_token(identity=user.id)
            return (
                jsonify(
                    {
                        "message": "Login successful",
                        "access_token": access_token,
                        "user": {"id": user.id, "username": user.username},
                    }
                ),
                200,
            )
        else:
            flash("Login successful", "success")
            return redirect(url_for("main.home"))

    # Invalid credentials
    if request.is_json:
        return jsonify({"message": "Invalid credentials"}), 401
    else:
        flash("Invalid credentials", "error")
        return redirect(url_for("main.home"))

    #     access_token = create_access_token(identity=user.id)
    #     return jsonify({"access_token": access_token, "api_key": user.api_key})
    # return jsonify({"message": "Invalid credentials"}), 401


@parser_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"success": True, "message": "API is alive"}), 200
