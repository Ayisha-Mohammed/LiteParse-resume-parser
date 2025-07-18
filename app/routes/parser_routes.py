from flask import Blueprint , request, jsonify
from app.services.parser_servies import parse_resume

parser_bp = Blueprint('parser', __name__)

@parser_bp.route('/parse',methods =['POST'])
def parse():
    resume_file=request.files.get('resume')

    if not resume_file:
        return jsonify({'error':'No resume uploaded'}),400
     
    result=parse_resume(resume_file)
    return jsonify(result )


