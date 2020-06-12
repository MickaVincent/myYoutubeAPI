from flask import Flask
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
import logging
# Import des variables contenant les routes
from api.routes.comment import comment_routes
from api.routes.user import user_routes
from api.routes.videos import videos_routes
from api.models.user import User
from api.models.videoformat import VideoFormat
from api.models.videos import Video
from api.models.token import Token
from api.models.comment import Comment
# Import pour la création de la BDD
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
# Import de la configuration de l'app
from api.config import config


app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    create_database(engine.url)

with app.app_context():
    db.create_all()

app.register_blueprint(user_routes)
app.register_blueprint(videos_routes)
app.register_blueprint(comment_routes)

@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


if __name__ == "__main__":
    app.run(port=5010, host="127.0.0.1", use_reloader=True)