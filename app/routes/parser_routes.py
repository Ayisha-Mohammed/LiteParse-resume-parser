from flask import (
    Blueprint,
    request,
    jsonify,
    # current_app
    render_template,
    redirect,
    url_for,
    session,
    flash,json,send_file
)
from io import BytesIO 
from app.services.res_parser import parse_resume
from app.limiter import limiter
from app import db, bcrypt
from app.models import User
from functools import wraps
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
    return render_template("home.html",user=session.get("user"),parsed_data=None)
@main_bp.route("/docs")
def docs():
    return render_template("docs.html")


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # auth header exists, use JWT
        auth_header = request.headers.get("Authorization",None)
        if auth_header and auth_header.startswith("Bearer"):
            try:
                verify_jwt_in_request()
                identity = get_jwt_identity()
                if not identity:
                    return jsonify({"success": False, "error": "JWT required"}),401
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 401
        else:
            # fallback to session-based auth
            if "user" not in session:
                flash("Please log in first.")
                return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return wrapper

# register
@parser_bp.route("/parse", methods=["POST"])
@auth_required
@limiter.limit("5 per minute")
def parse():
    try:
        resume_file = request.files.get("resume")
        # check if API request json/browser
        is_api_request = request.is_json or request.headers.get("Accept") == "application/json"
        if not resume_file:
            msg = "No resume uploaded."
            if is_api_request:
                return jsonify({"success": False, "error": msg}), 400
            else:
                flash(msg, "error")
                return redirect(url_for("main.home"))

        # Parse resume
        try:
            result = parse_resume(resume_file)
        except Exception as parse_err:
            print("Parser error:", parse_err)
            msg = "Failed to parse resume. Check file format."
            if is_api_request:
                return jsonify({"success": False, "error": msg}), 500
            else:
                flash(msg, "error")
                return redirect(url_for("main.home"))

        # Handle known parser errors returned as>>dict
        if isinstance(result, dict) and result.get("error"):
            msg = result["error"]
            if is_api_request:
                return jsonify({"success": False, "error": msg}), 400
            else:
                flash(msg, "error")
                return redirect(url_for("main.home"))

        # store parsed data in session (for browser download)
        session["parsed_data"] = result

        # response
        if is_api_request:
            #return full result dict for API , always.
            return jsonify({"success": True, "data": result}), 200
        
        return render_template(
            "home.html",
            parsed_data=result,
            user=session.get("user")
        )

    except Exception as e:
        print("Unexpected error:", e)
        if is_api_request:
            return jsonify({"success": False, "error": str(e)}), 500
        flash("Something went wrong while parsing the resume.", "error")
        return redirect(url_for("main.home"))

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
        msg = "Email, password, and username are required."
        if request.is_json:
            return jsonify({"message": msg}), 400
        else:
            flash(msg, "error")
            return redirect(url_for("main.home"))

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        msg = "User already exists."
        if request.is_json:
            return jsonify({"message": msg}), 400
        else:
            flash(msg, "error")
            return redirect(url_for("main.home"))

    # Create user
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    # # Log in user (session)
    # session['user'] = {"id": user.id, "username": user.username} ......... no need in reg rn !.

    if request.is_json:
        return jsonify({"message": "User created", "api_key": user.api_key}), 201
    else:
        flash("Registration successful!", "success")
        return redirect(url_for("main.home"))


# Login
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
            access_token = create_access_token(identity=str(user.id))
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
    # ..changed this to session based access(flasks-client side signed cookie session)

# Logout     
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)  # remove user from session
    flash("Logged out successfully", "success")
    return redirect(url_for("main.home")) 

#Download output
@parser_bp.route("/download_parsed")
def download_parsed():
    data = session.get("parsed_data")
    if not data:
        flash("No parsed data available for download","error")
        return redirect(url_for("main.home"))

    json_bytes = json.dumps(data, indent=4).encode("utf-8")
    return send_file(
        BytesIO(json_bytes),
        mimetype="application/json",
        as_attachment=True,
        download_name="parsed_resume.json"
    )

#Ping Check
@parser_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"success": True, "message": "API is alive"}), 200