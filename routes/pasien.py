from middleware.authorization import token_required
import flask
import models

router = flask.Blueprint("pasien",__name__)

@router.route("/", methods=["GET"])
@token_required(["pasien"])
def testrouter(current_user):
    return flask.make_response(flask.jsonify(message="test pasien route"))