from .. import db
from .models import Reviews
from ..movies.models import Movie


def create_review(movies_id, title, content, rating, user_id):
    movie = Movie.query.get(movies_id)
    if not movie:
        return {'message': 'Movie not found'}, 404
    review = Reviews(
        title=title,
        content=content,
        rating=rating,
        user_id=user_id,
        movies_id=movies_id
    ) 
    db.session.add(review)
    db.session.commit()
    return {'message': 'Review created successfully'}, 201

def get_reviews(movies_id):
    movie = Movie.query.get(movies_id)
    if not movie:
        return {'message': 'Movie not found'}, 404
    reviews = Reviews.query.filter_by(movies_id=movies_id).all()
    return {'reviews': [r.serialize() for r in reviews]}

def update_review(review_id, user_id, new_data):
    review = Reviews.query.get(review_id)
    if not review:
        return {'message': 'Review not found'}, 404
    if review.user_id != user_id:
        return {'message': 'Unauthorized'}, 401
    review.Title = new_data.get('title', review.Title)
    review.Content = new_data.get('content', review.Content)
    review.Rating = new_data.get('rating', review.Rating)
    db.session.commit()
    return {'message': 'Review updated successfully'}

def delete_review(review_id, user_id):
    review = Reviews.query.get(review_id)
    if not review:
        return {'message': 'Review not found'}, 404
    if review.user_id != user_id:
        return {'message': 'Unauthorized'}, 401
    db.session.delete(review)
    db.session.commit()
    return {'message': 'Review deleted successfully'}

