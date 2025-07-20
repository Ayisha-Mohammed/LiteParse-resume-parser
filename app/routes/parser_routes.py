from flask import Blueprint , request, jsonify
from app.services.res_parser import parse_resume

parser_bp = Blueprint('parser', __name__)


@parser_bp.route('/parse',methods =['POST'])
def parse():
    resume_file=request.files.get('file')
    if not resume_file:
        return jsonify({'error':'No resume uploaded'}),400
    else:
        print("Uploaded Your file :",resume_file.filename)
     
    result_of_parsed_resume=parse_resume(resume_file)
    return jsonify(result_of_parsed_resume)


