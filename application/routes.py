from flask import jsonify, Blueprint

main = Blueprint("main", __name__)

@main.route('/')
def hello():
    return jsonify({
        "message": "Welcome to the Reddy 43 - Movies Application",
        "description": "Movies API",
        "endpoints": [
            "GET / 200|500",
            "GET /movies",
            "GET /movies/<int:id>",
            "GET /movies/top",
            "GET /movies/recent",
            "GET /genres"
        ]
    }), 200

@main.route('/profile')
def profile():
    return 'Profile'
