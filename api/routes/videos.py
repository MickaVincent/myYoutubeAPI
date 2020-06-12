from flask import Blueprint
from flask import request, render_template
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.videos import Video
from api.models.videoformat import VideoFormat
from api.utils.database import db
from api.models.user import User
from moviepy.editor import VideoFileClip
from api.utils.validate_uuid import is_valid_uuid
from api.utils.token_decorator import token_required
import os
import uuid

videos_routes = Blueprint("videos_routes", __name__)


def allowed_file(filename):
    app = db.get_app()
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@videos_routes.route('/', methods=['GET'])
def testing():
    return render_template('public/index.html')


@videos_routes.route('/videos', methods=['GET'])
def get_all_videos():
    try:
        data = request.get_json()
        if isinstance(data, dict):
            videos = db.session.query(Video)
            pager = []
            output = []

            if 'name' in data:
                if isinstance(data['name'], str):
                    videos = videos.filter(Video.name.contains(data['name']))
                else:
                    return response_with(resp.INVALID_INPUT_422)

            if 'duration' in data:
                if isinstance(data['duration'], int):
                    videos = videos.filter_by(duration=data['duration'])
                else:
                    return response_with(resp.INVALID_INPUT_422)

            if 'user' in data:
                if isinstance(data['user'], str):
                    if is_valid_uuid(data['user']):
                        videos = videos.filter_by(user_uuid=(data['user']))
                    else:
                        videos = videos.join(User).filter(User.username == data['user'])
                else:
                    return response_with(resp.INVALID_INPUT_422)

            if 'perPage' in data and 'page' in data:
                if isinstance(data['perPage'], int) and isinstance(data['page'], int):
                    videos = videos.paginate(page=data['page'], per_page=data['perPage'])
                    for video in videos.items:
                        output.append(video.get_as_dict())
                else:
                    return response_with(resp.INVALID_INPUT_422)
                pager = {
                    "current": data['page'],
                    "total": videos.pages
                }
                return response_with(resp.SUCCESS_200, value={"data": output, "pager": pager})
            else:
                video = videos.all()
                for video in videos:
                    output.append(video.get_as_dict())

            return response_with(resp.SUCCESS_200, value={"data": output})
        else:
            return response_with(resp.MISSING_PARAMETERS_422)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_500)


@videos_routes.route('/video/<id>', methods=['DELETE'])
@token_required
def delete_video(current_user, id):
    print(id)
    video = db.session.query(Video).filter_by(uuid=id).first()

    try:
        os.rename(video.source, video.source)
    except OSError as e:
        print(e)
        print("Cannot touch file {0}, must a problem in filesystem".format(video.source))
        return response_with(resp.SERVER_ERROR_500)
    except AttributeError as e:
        print(e)
        print("Didn't found video")
        return response_with(resp.SERVER_ERROR_404)

    try:
        video.delete()
    except Exception as e:
        print(e)
        print("Cannot remove data from Database, aborting.")
        return response_with(resp.SERVER_ERROR_500)

    try:
        os.remove(video.source)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_500)

    return response_with(resp.NO_CONTENT_204)


@videos_routes.route('/video/<uuid>', methods=['PUT'])
@token_required
def update_video(current_user, uuid):

    data = request.get_json()
    video = db.session.query(Video).filter_by(uuid=uuid).first()
    user = db.session.query(User)

    if data is None:
        return response_with(resp.BAD_REQUEST_400)

    try:
        if 'name' in data and 'user' in data:
            if user.filter_by(uuid=data['user']).first():
                video.update_name(data['name'])
                video.update_user(data['user'])
                return response_with(resp.SUCCESS_200, {"data": video.get_as_dict()})
            else:
                return response_with(resp.INVALID_INPUT_422)
        else:
            return response_with(resp.MISSING_PARAMETERS_422)
 
    except Exception as e:
        print(e)
        return response_with(resp.BAD_REQUEST_400)

@videos_routes.route('/user/<public_id>/video', methods=["GET", "POST"])
@token_required
def create_video(current_user, public_id):
    app = db.get_app()
    user = db.session.query(User).filter_by(uuid=public_id).first()
    data = request.get_json()

    if not user:
        return response_with(resp.BAD_REQUEST_400)

    if current_user.uuid != public_id:
        return response_with(resp.UNAUTHORIZED_403)

    if request.method == "POST":

        if request.files:
            video_content = request.files["source"]
            video_name = request.form["name"]

            if video_content and allowed_file(video_content.filename):
                public_vid = str(uuid.uuid4()) + "." + str(video_content.filename.split('.')[1])
                user_folder = app.config["VIDEO_FOLDER"] + str(public_id) + '/'

                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)

                source_and_name = os.path.join(user_folder, public_vid)

                video_content.save(source_and_name)
                
                # Fetch video duration
                clip = VideoFileClip(source_and_name)
                du = int(clip.duration)

                #  Create video row
                video = Video(name=video_name, duration=du, user_uuid=public_id, source=source_and_name, enabled=True)
                video.create()
            else:
                return response_with(resp.INVALID_INPUT_422)

            return response_with(resp.SUCCESS_201, value={"message": "Ok", "data": video.get_as_dict()})
        else:
            return response_with(resp.INVALID_INPUT_422)
    else:
        return render_template("public/upload_template.html",
                               uuid=public_id,
                               action="/user/" + public_id + "/video"
                               )


@videos_routes.route('/user/<public_id>/videos', methods=['GET'])
def get_all_videos_by_user(public_id):

    try:
        user = db.session.query(User).filter_by(uuid=public_id).first()
        if not user:
            return response_with(resp.SERVER_ERROR_404)

        data = request.get_json()
        if data is None:
            return response_with(resp.BAD_REQUEST_400)
        videos = []
        output = []

        if 'page' in data and 'perPage' in data and data['page'] is not None and data['perPage'] is not None:
            if isinstance(data['page'], int) and isinstance(data['perPage'], int):
                videos = db.session.query(Video).filter_by(user_uuid=public_id)
                videos = videos.paginate(page=data['page'], per_page=data['perPage'])
                for video in videos.items:
                    output.append(video.get_as_dict())
                pager = {
                    "current": data['page'],
                    "total": videos.pages
                }
                return response_with(resp.SUCCESS_200, value={"data": output, "pager": pager})
            else:
                return response_with(resp.INVALID_INPUT_422)
        else:
            return response_with(resp.BAD_REQUEST_400)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_500)


@videos_routes.route('/video/<public_id>', methods=['PATCH'])
def encoding_video_by_id(public_id):
    data = request.get_json()
    if "format" not in data:
        return response_with(resp.MISSING_PARAMETERS_422)
    if "file" not in data:
        return response_with(resp.MISSING_PARAMETERS_422)

    video = db.session.query(Video).filter_by(uuid=public_id).first()
    if video is None:
        return response_with(resp.SERVER_ERROR_404)

    video_format = VideoFormat(code=data['format'], uri=data['file'], video_uuid=public_id)
    video_format.create()

    return response_with(resp.SUCCESS_200, value={"data": video.get_as_dict()})
