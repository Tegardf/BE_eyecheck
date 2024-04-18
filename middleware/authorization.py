from functools import wraps
import jwt, os
from flask import request
from models.model import Users
from models.database import session

def token_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*arg, **kwargs):
            if ("Authorization" in request.headers) == False:
                return {
                    "message": "request error",
                }, 400
            token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            try:
                data = jwt.decode(token, key=os.getenv('JWT_KEY'), algorithms='HS256')
                current_user = session.query(Users).filter_by(username = data['username']).first()
                session.close()
                try:
                    role.index(current_user.role)
                except Exception as r:
                    return {
                        "message": "role tidak sesuai",
                    }, 401

            except Exception as e:
                if str(e) == 'Signature has expired':
                    return {
                        "message": "token expired",
                    }, 407
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500
            return f(current_user, *arg, *kwargs)
        return decorated
    return decorator