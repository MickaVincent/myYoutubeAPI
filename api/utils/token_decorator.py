from flask import request
from api.models.user import User
from api.models.token import Token
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.database import db
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_str = None

        if 'Authorization' in request.headers:
            token_str = request.headers['Authorization']

        if not token_str:
            return response_with(resp.UNAUTHORIZED_403)

        try:
            token = db.session.query(Token).filter_by(code=token_str).first()
            if token.check_validity():
                current_user = db.session.query(User).filter_by(uuid=token.user_uuid).first()
            else:
                print("Token expired")
                return response_with(resp.UNAUTHORIZED_403)
        except:
            return response_with(resp.UNAUTHORIZED_403)

        return f(current_user, *args, **kwargs)

    return decorated