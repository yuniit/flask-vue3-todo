from flask import Flask
from db import Connection
from config import Config
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()
login_manager.login_view = "auth.login"

db = Connection("flask_mongo_db")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'rabbit_tech'
    CORS(app)
    login_manager.init_app(app)
    app.config.from_object(Config)

    ## register blueprint
    from app.auth import bp as auth_bp
    from app.todo import bp as todo_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(todo_bp, url_prefix="/todo")

    @app.route("/", methods=("GET", "POST"))
    def index():
        return "hello world"

    return app
