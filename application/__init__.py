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
    
   
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

    db.init_app(app)
    
    app.app_context().push()


    from application.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from application.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)


    from application.movies.routes import movies_blueprint as movies_blueprint
    app.register_blueprint(movies_blueprint)

    from application.recommendations_list.routes import recommendations_blueprint
    app.register_blueprint(recommendations_blueprint)

    from application.user_films_list.routes import user_film_list_blueprint
    app.register_blueprint(user_film_list_blueprint)

    from application.reviews.routes import reviews_bp
    app.register_blueprint(reviews_bp)


    #This is required to call methods like create_access_toke() and others from Flask-JWT-Extended
    jwt = JWTManager(app)

    return app
    # from application import routes
