from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug import exceptions
from .models import RecommendationsList
from .. import db
from ..movies.models import Movie
from ..recommendation.controllers import load_movie_dataset, recommend_movie
from flask import g
import re


def get_movie_title(movie_id):
    load_movie_dataset()
    movie = g.movie_dataset.loc[movie_id]

    if not movie.empty:
        return {"title": movie["title"]}
    else:
        return {"message": f"Movie with movie_id {movie_id} not found"}


def index():
    try:
        movies = RecommendationsList.query.filter_by(user_id=get_jwt_identity())
        return jsonify({"data": [c.json for c in movies]}), 200
    except Exception as e:
        print(e)
        raise exceptions.InternalServerError(f"We are working on it")


def show(id):
    movie_list = RecommendationsList.query.filter_by(id=id).first()
    try:
        list_of_movie_ids = movie_list.movie_ids.split(";")

        return jsonify({"title": movie_list.title,
                        "movies": [get_movie_title(int(movie_id)) for movie_id in list_of_movie_ids[:-1]], "movies_id":list_of_movie_ids[:-1]}), 200
    except Exception as e:
        print(e)
        raise exceptions.NotFound(f"You get it")


def create():
    try:
        title = request.json.get("title", None)
        print()
        # new_movie_list = UserFilmList(get_jwt_identity(),title,[])
        new_movie_list = RecommendationsList(get_jwt_identity(), title, "")

        db.session.add(new_movie_list)
        db.session.commit()

        return jsonify({"data": new_movie_list.json}), 201
    except Exception as e:
        print(e)
        raise exceptions.BadRequest(f"We cannot process your request")


def update(id):
    try:
        data = request.json
        movie_list = RecommendationsList.query.filter_by(id=id, user_id=get_jwt_identity()).first()
        if movie_list is None:
            return jsonify({"message": "Movie list is not found"}), 404

        for (attribute, value) in data.items():
            if hasattr(movie_list, attribute):
                setattr(movie_list, attribute, value)

        db.session.commit()
        return jsonify({"data": movie_list.json}), 201
    except Exception as e:
        print(e)
        raise exceptions.BadRequest(f"We cannot update")


def destroy(id):
    try:
        movie_list = RecommendationsList.query.filter_by(id=id, user_id=get_jwt_identity()).first()
        if movie_list is None:
            return jsonify({"message": "Movie list is not found"}), 404

        db.session.delete(movie_list)
        db.session.commit()
        return jsonify({"message": "Movie list Deleted"}), 204
    except Exception as e:
        print(e)
        raise exceptions.BadRequest(f"We cannot delete the list of movies")


def recommend(id):
    movie_list = RecommendationsList.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if movie_list is None:
        return jsonify({"message": "Movie list is not found"}), 404

    new_movie_id = recommend_movie(movie_list.movie_ids)
    if (new_movie_id==-1):
        return jsonify({"message": "Please add a fav movie in the list"}), 404
    movie_list.movie_ids = movie_list.movie_ids + str(new_movie_id) + ";"
    db.session.add(movie_list)
    db.session.commit()
    return jsonify({"message": "Movie recommended successfully"}), 200


def show_movie_details(id, movie_id):
    load_movie_dataset()
    movie = g.movie_dataset.loc[movie_id]

    if not movie.empty:
        return jsonify({"title": movie["title"],
                        "genres": movie["genres"],
                        "release_date": movie["release_date"],
                        "overview": movie["overview"]}), 200
    else:
        return jsonify({"message": f"Movie with movie_id {movie_id} not found"}), 404


def add_movie(id, movie_id):
    movie_list = RecommendationsList.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if movie_list is None:
        return jsonify({"message": "Movie list is not found"}), 404

    movie_list.movie_ids = movie_list.movie_ids + str(movie_id) + ";"
    db.session.add(movie_list)
    db.session.commit()
    return jsonify({"message": "Movie added successfully"}), 200


def remove_movie(id, movie_id):
    user_film_instance = RecommendationsList.query.get(id)

    if user_film_instance:
        movie_id_str = str(movie_id) + ";"
        user_film_instance.movie_ids = user_film_instance.movie_ids.replace(movie_id_str, "")
        db.session.commit()
        return jsonify({"message": "Movie removed successfully"}), 200

    else:
        return jsonify({"message": "UserFilmList not found"}), 404


def search():
    text = request.json.get("text", None)
    load_movie_dataset()
    movies_list = g.movie_dataset[g.movie_dataset["title"].str.contains(text, na=False, flags=re.IGNORECASE)]

    if movies_list.empty:
        return jsonify({"message": "Movie not found"}), 404
    else:
        return jsonify({"movies":
                            [{"title": movie["title"],
                              "movie_id": movie["index"],
                              "genres": movie["genres"],
                              "release_date": movie["release_date"],
                              "overview": movie["overview"]} for index, movie in movies_list.iterrows()]}), 200
