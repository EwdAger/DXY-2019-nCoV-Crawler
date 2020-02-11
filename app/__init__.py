# """
#     Desc:
#     Auth: Robinsen
#     Date: 2019/4/30 10:24
# """
from flask_cors import CORS

from app.app import Flask


def register_blueprint(application):
    from app.api import create_blueprint_v1
    application.register_blueprint(create_blueprint_v1(), url_prefix="/api")


def create_app():
    application = Flask(__name__)
    CORS(application, supports_credentials=True)  # 设置允许跨域
    application.config.from_object('app.config.setting')
    register_blueprint(application)
    # register_plugin(application)
    return application
