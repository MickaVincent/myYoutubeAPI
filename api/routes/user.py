from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.user import User
from api.models.token import Token
from api.utils.database import db
from werkzeug.security import check_password_hash
from api.utils.token_decorator import token_required


user_routes = Blueprint("user_authors", __name__)


@user_routes.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if 'pseudo' not in data or data['pseudo'] is None:
            data['pseudo'] = ""
        if 'username' in data and 'email' in data and 'password' in data:
            user = User(username=data['username'], email=data['email'], password=data['password'], pseudo=data['pseudo'])
            user.create()
            return response_with(resp.SUCCESS_201, value={"user": user.get_as_dict(isOwner=True)})
        else:
            return response_with(resp.MISSING_PARAMETERS_422)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/auth', methods=['POST'])
def user_auth():
    auth = request.authorization
    if auth.username is None:
        return response_with(resp.MISSING_PARAMETERS_422)
    try:
        user = db.session.query(User).filter_by(username=auth.username).first()
        if(check_password_hash(user.password, auth.password)):
            token = Token(user_uuid=user.uuid)
            token.create()
            return response_with(resp.SUCCESS_201, value={"data": token.get_as_dict()})
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        print(e)
        return response_with(resp.UNAUTHORIZED_403)


@user_routes.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if current_user.uuid != public_id:
        return response_with(resp.UNAUTHORIZED_403)
    try:
        user = db.session.query(User).filter_by(uuid=public_id).first()
        user.delete()
        return response_with(resp.SUCCESS_201)
    except Exception as e:
        print(e)
        return response_with(resp.BAD_REQUEST_400)


@user_routes.route('/users', methods=['GET'])
def get_all_users():
    try:
        data = request.get_json()
        if isinstance(data, dict):
            users = db.session.query(User)

            pager = []
            output = []

            if 'pseudo' in data:
                if isinstance(data['pseudo'], str):
                    users = users.filter(User.pseudo.contains(data['pseudo']))
                else:
                    return response_with(resp.INVALID_INPUT_422)

            if 'perPage' in data and 'page' in data:
                if isinstance(data['page'], int) and isinstance(data['perPage'], int):
                    users = users.paginate(page=data['page'], per_page=data['perPage'])
                    for user in users.items:
                        output.append(user.get_as_dict())
                    pager = {
                        "page": data['page'],
                        "total": users.pages
                    }
                else:
                    return response_with(resp.INVALID_INPUT_422)
            if not output or not pager:
                return response_with(resp.MISSING_PARAMETERS_422)

            return response_with(resp.SUCCESS_200, value={"data": output, "pager": pager})
        else:
            return response_with(resp.MISSING_PARAMETERS_422)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_404)


@user_routes.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user, public_id):
    try:
        user = db.session.query(User).filter_by(uuid=public_id).first()
        if current_user.uuid == user.uuid:
            return response_with(resp.SUCCESS_200, value={"data": user.get_as_dict(True)})
        else:
            return response_with(resp.SUCCESS_200, value={"data": user.get_as_dict()})

    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_404)


@user_routes.route('/user/<public_id>', methods=['PUT'])
@token_required
def update_user(current_user, public_id):
    if current_user.uuid != public_id:
        return response_with(resp.UNAUTHORIZED_403)
    try:
        data = request.get_json()
        user = db.session.query(User).filter_by(uuid=public_id).first()

        if 'username' in data:
            user.update_username(data['username'])

        if 'pseudo' in data:
            user.update_pseudo(data['pseudo'])

        if 'email' in data:
            user.update_email(data['email'])

        if 'password' in data:
            user.update_password(data['password'])

        return response_with(resp.SUCCESS_200, {"data": user.get_as_dict(True)})

    except Exception as e:
        print(e)
        return response_with(resp.BAD_REQUEST_400)
