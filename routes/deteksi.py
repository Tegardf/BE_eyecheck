from flask import make_response, jsonify, request, Blueprint
from middleware.authorization import token_required

router = Blueprint("deteksi",__name__)

@router.route("/", methods=["GET"])
def testrouter():
    return make_response(jsonify(message="test deteksi route"))

@router.route("/svm", methods=["POST"])
@token_required(["dokter","pasien"])
def svm(current_user):
    
    return make_response(jsonify(message="test SVM"),200)
