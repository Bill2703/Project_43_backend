from flask import jsonify
from werkzeug import exceptions
from .models import Movie, Genre
import requests
from .. import db
import random

def index_and_seed(total_pages=10):
    base_url = "https://api.themoviedb.org/3/movie/now_playing"
    language = "en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OWRlYzM5ZWEzOTk3ZWRlNzJkOGJmYmE3ODliNmNhMSIsInN1YiI6IjY1OWZjMTI2NTI5NGU3MDEyYmM1OTRhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-BESHu0oI5-ndoVrFpgPq3FUd5Hs1cVyu7JLugdsHzE" 
    }

    # Clear existing data in the movies table
    Movie.query.delete()

    # Seed movies into the database from multiple pages
    for page in range(1, total_pages + 1):
        params = {"language": language, "page": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            for movie_data in data.get('results', []):
                movie = Movie(
                    original_title=movie_data.get('original_title'),
                    original_language=movie_data.get('original_language'),
                    overview=movie_data.get('overview'),
                    vote_average=movie_data.get('vote_average'),
                    release_date=movie_data.get('release_date'),
                    poster_path=movie_data.get('poster_path'),
                    genre_ids=movie_data.get('genre_ids'),
                )

                movie.poster_path = movie.poster_url
                db.session.add(movie)

    # Commit the changes to the database after all pages are processed
    db.session.commit()

    return jsonify({"message": f"Seeded {total_pages} pages of movies into the database"})




def index():
    movies = Movie.query.all()

    movies_list = [movie.json for movie in movies]

    return jsonify(movies_list)


def show(id):
    
    movie = Movie.query.get(id)

    if movie is None:
        raise exceptions.NotFound("Movie not found")

    return jsonify(movie.json)


# def get_random_movie_by_genre(genre_id):
#     try:
#         genre = Genre.query.get(genre_id)
#         if genre is None:
#             raise exceptions.NotFound("Genre not found")

#         movies_in_genre = genre.movies  # Remove the parentheses here

#         if not movies_in_genre:
#             raise exceptions.NotFound(f"No movies found for the specified genre (ID: {genre_id})")

#         random_movie = random.choice(movies_in_genre)

#         return jsonify(random_movie.json)

#     except Exception as e:
#         return {"error": str(e)}, 500


def top_rated():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OWRlYzM5ZWEzOTk3ZWRlNzJkOGJmYmE3ODliNmNhMSIsInN1YiI6IjY1OWZjMTI2NTI5NGU3MDEyYmM1OTRhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-BESHu0oI5-ndoVrFpgPq3FUd5Hs1cVyu7JLugdsHzE"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def upcoming():
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OWRlYzM5ZWEzOTk3ZWRlNzJkOGJmYmE3ODliNmNhMSIsInN1YiI6IjY1OWZjMTI2NTI5NGU3MDEyYmM1OTRhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-BESHu0oI5-ndoVrFpgPq3FUd5Hs1cVyu7JLugdsHzE"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def genres():
    genres = Genre.query.all()

    genres_list = [genre.json for genre in genres]

    return jsonify(genres_list)

def genres_and_seed():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OWRlYzM5ZWEzOTk3ZWRlNzJkOGJmYmE3ODliNmNhMSIsInN1YiI6IjY1OWZjMTI2NTI5NGU3MDEyYmM1OTRhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-BESHu0oI5-ndoVrFpgPq3FUd5Hs1cVyu7JLugdsHzE"
    }


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for genre_data in data.get('genres', []):
            genre = Genre(
                id=genre_data.get('id'),
                name=genre_data.get('name')
            )
            db.session.add(genre)
    
    db.session.commit()

    return jsonify({"message": "Success"})


    


