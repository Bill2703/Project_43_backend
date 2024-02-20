from application.movies.models import Movie

def test_new_movie():
    movie = Movie(original_language='en', original_title='Test', overview='jkljkl', vote_average=6.12, release_date=2023-11-22, poster_path="https://image.tmdb.org/t/p/w500/jE5o7y9K6pZtWNNMEw3IdpHuncR.jpg", genre_ids={36,10752,18})
    
    assert movie.original_language == 'en'
    assert movie.original_title == 'Test'
    assert movie.overview == 'jkljkl'
    assert movie.vote_average == 6.12
    assert movie.release_date == 2023-11-22
    assert movie.poster_path == "https://image.tmdb.org/t/p/w500/jE5o7y9K6pZtWNNMEw3IdpHuncR.jpg"
    assert movie.genre_ids == {36,10752,18}