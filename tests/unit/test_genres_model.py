from application.movies.models import Genre

def test_new_genre():
    genre = Genre(id=28, name='Action')
    
    assert genre.id == 28
    assert genre.name == 'Action'