from flask import Blueprint , request, jsonify , current_app
from app.services.res_parser import parse_resume
from app.limiter import limiter 


parser_bp = Blueprint('parser', __name__)
@parser_bp.route('/parse', methods=['POST'])
@limiter.limit("5 per minute") 
def parse():
    try:
        resume_file = request.files.get('file')
        if not resume_file:
            return jsonify({'success': False, 'error': 'No resume uploaded'}), 400
        current_app.logger.info(f"Uploaded file: {resume_file.filename}")
        print("Uploaded Your file:", resume_file.filename)
        result_of_parsed_resume = parse_resume(resume_file)

        # Handle known errors returned from parser
        if isinstance(result_of_parsed_resume, dict) and result_of_parsed_resume.get("error"):
            return jsonify({'success': False, 'error': result_of_parsed_resume['error']}), 400

        return jsonify({'success': True, 'data': result_of_parsed_resume}), 200

    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({'success': False, 'error': 'Internal Server Error', 'details': str(e)}), 500


@parser_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"success": True, "message": "API is alive"}), 200