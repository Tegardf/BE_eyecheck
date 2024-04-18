from middleware.authorization import token_required
import flask
import models


router = flask.Blueprint("dokter",__name__)

@router.route("/", methods=["GET"])
@token_required(["dokter"])
def testrouter(current_user):
    return flask.make_response(flask.jsonify(message="test dokter route"))