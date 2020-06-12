from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.comment import Comment
from api.utils.database import db
from api.utils.token_decorator import token_required


comment_routes = Blueprint("comment_routes", __name__)


@comment_routes.route('/video/<uuid>/comment', methods=['POST'])
@token_required
def create_comment(current_user, uuid):
    try:
        data = request.get_json()

        if 'body' in data:
            comment = Comment(body=data['body'], user_uuid=current_user.uuid, video_id=uuid)
            comment.create()
            return response_with(resp.SUCCESS_201, value={'data': comment.get_as_dict()})
        else:
            return response_with(resp.MISSING_PARAMETERS_422)
        return
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_500)

@comment_routes.route('/video/<id>/comments', methods=['GET'])
def get_comment_list(id):
    try:
        data = request.get_json()
        comments = db.session.query(Comment).filter_by(video_id=id)
        output = []
        pager = []

        if 'perPage' in data and 'page' in data:
            comments = comments.paginate(page=data['page'], per_page=data['perPage'])
            for comment in comments.items:
                output.append(comment.get_as_dict())
            pager = {
                "page": data['page'],
                "total": comments.pages
            }

        else:
            comment = comments.all()
            for comment in comments:
                output.append(comment.get_as_dict())
            return response_with(resp.SUCCESS_200, value={"data": output})

        return response_with(resp.SUCCESS_200, value={"data": output, "pager": pager})

    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_500)