from application.reviews.models import Reviews

def test_new_review():
    review = Reviews(title='Average', content='Not too bad actually', rating=5, user_id=1, movies_id=1)
    
    assert review.Title == 'Average'
    assert review.Content == 'Not too bad actually'
    assert review.Rating == 5
    assert review.user_id == 1
    assert review.movies_id == 1