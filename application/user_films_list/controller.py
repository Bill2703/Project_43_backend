from flask import jsonify, request
from .. import db
from .models import UserFilmList
from application.movies.models import Movie
from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required()
def add_to_user_list():
    user_id = get_jwt_identity()
    print(user_id)
    data = request.json
    movies_id = data.get('movies_id')
    user_film_list = UserFilmList(user_id=user_id, movies_id=movies_id)
    db.session.add(user_film_list)
    db.session.commit()
    return jsonify({"message": "Movie added to user's film list successfully"})

@jwt_required()
def remove_from_user_list():
    user_id = get_jwt_identity()
    data = request.json
    movies_id = data.get('movies_id')
    user_film_list_item = UserFilmList.query.filter_by(user_id=user_id, movies_id=movies_id).first()

    if user_film_list_item:
        db.session.delete(user_film_list_item)
        db.session.commit()
        return jsonify({"message": "Movie removed from user's film list successfully"})
    else:
        return jsonify({"message": "Movie not found in user's film list"})

@jwt_required()
def get_user_film_list():
    user_id = get_jwt_identity()
    user_film_list = UserFilmList.query.filter_by(user_id=user_id).all()
    movies = [Movie.query.get(item.movies_id).json for item in user_film_list]
    return jsonify(movies)

