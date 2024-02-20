from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import (
    create_review,
    get_reviews,
    update_review,
    delete_review
)

# Create a blueprint
reviews_bp = Blueprint('reviews', __name__)

# Create review
@reviews_bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review_route():
    data = request.json
    movies_id = data.get('movies_id')
    title = data.get('title')
    content = data.get('content')
    rating = data.get('rating')
    user_id = get_jwt_identity()
    result = create_review(movies_id, title, content, rating, user_id)
    return jsonify(result)

# Get reviews
@reviews_bp.route('/reviews/<int:movies_id>', methods=['GET'])
def get_reviews_route(movies_id):
    result = get_reviews(movies_id)
    return jsonify(result)

# Update reviews
@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review_route(review_id):
    new_data = request.json
    user_id = get_jwt_identity()
    result = update_review(review_id, user_id, new_data)
    return jsonify(result)

# Delete review
@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review_route(review_id):
    user_id = get_jwt_identity()
    result = delete_review(review_id, user_id)
    return jsonify(result)
