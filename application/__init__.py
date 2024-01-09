from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(env=None):
    load_dotenv()
    app = Flask(__name__)
    app.json_provider_class.sort_keys = False
    CORS(app)
    print("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

    db.init_app(app)
    print(os.environ["SQLALCHEMY_DATABASE_URI"])
    app.app_context().push()

    from application.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from application.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from application.user_film_list.routes import movies_list
    app.register_blueprint(movies_list)

    #This is required to call methods like create_access_toke() and others from Flask-JWT-Extended
    jwt = JWTManager(app)

    return app
    # from application import routes
