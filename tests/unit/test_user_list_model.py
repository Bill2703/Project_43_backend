from application.user_films_list.models import UserFilmList

def test_new_user_list():
    user_list = UserFilmList(user_id=2, movies_id=199)
    
    assert user_list.user_id == 2
    assert user_list.movies_id == 199