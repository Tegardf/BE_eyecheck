from flask import make_response, jsonify, request, Blueprint
from models import model
from models.database import session
import bcrypt, jwt, datetime, os

router = Blueprint("auth",__name__)

@router.route("/", methods=["GET"])
def testrouter():
    return make_response(jsonify(message="test auth route"))

@router.route("/login", methods = ["POST"])
def login():
    usernameV = request.json['username']
    passwordV = request.json['password'].encode('utf-8')
    if (usernameV and passwordV) == False:
        return make_response(jsonify(message="request tidak cocok"),422)
    try:
        user = session.query(model.Users).filter_by(username = usernameV).first()
        checkPwd = bcrypt.checkpw(passwordV, user.password.encode('utf-8'))
        if (user and checkPwd) == False:
            return make_response(jsonify(message="user belum register"),401)
        token = jwt.encode({
            'username': user.username,
            'exp'  : datetime.datetime.utcnow() + datetime.timedelta(days=1),
        }, os.getenv('JWT_KEY'), algorithm='HS256')
        print (datetime.datetime.utcnow() + datetime.timedelta(seconds=1))
        return make_response(jsonify({
            'message' : "Berhasil Login",
            'token' : token
        }),200)
    except Exception as e:
        return make_response(jsonify({'message' : "error", 'error':str(e)}),500)
    
@router.route("/register", methods = ["POST"])
def register():
    usernameV = request.json['username']
    roleV = request.json['role']
    passwordV = request.json['password'].encode('utf-8')
    if (usernameV and roleV and passwordV) == False:
        return make_response(jsonify(message="request tidak cocok"),422)
    try:
        user = session.query(model.Users).filter_by(username = usernameV).first()
        if user:
            return make_response(jsonify(message="user sudah ada"),400)
        hashPassword = bcrypt.hashpw(passwordV, bcrypt.gensalt())
        hashPassword = hashPassword.decode("utf-8")
        addNewuser = model.Users(username = usernameV, password = hashPassword, role = roleV)
        try:
            session.add(addNewuser)
            session.commit()
            session.close()
            return make_response(jsonify(message="Regis berhasil"),201)
        except Exception as e:
            session.rollback()
            return make_response(jsonify(message="Regis Gagal", errors = str(e)))
    except Exception as e:
        return make_response(jsonify({'message' : "error", 'error':str(e)}),500)