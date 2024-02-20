import requests
from random import randrange

ENDPOINT = "http://localhost:4000/movies"
GENRE_ENDPOINT = "http://localhost:4000/genres"

response = requests.get(ENDPOINT)
print(response)

data = response.json()
print(data)

status_code = response.status_code
print(status_code)

# GET /movies
def test_index():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

# GET /movies:id
def test_show():
    movie_id = randrange(1, 201)
    show_movie_id = requests.get(ENDPOINT + f"/{movie_id}")
    assert show_movie_id.status_code == 200

# GET /movies/top
def test_top_movies():
    top_movies = requests.get(ENDPOINT + f"/top") 
    assert top_movies.status_code == 200

# GET /movies/recent
def test_recent_movies():
    recent_movies = requests.get(ENDPOINT + f"/recent") 
    assert recent_movies.status_code == 200

# GET /genres
def test_genres():
    genres = requests.get(GENRE_ENDPOINT)
    assert genres.status_code == 200