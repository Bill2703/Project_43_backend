from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from werkzeug import exceptions
from .controllers import index, create, show, update, destroy,show_movie_details,add_movie,remove_movie,recommend,search

recommendations_blueprint = Blueprint("recommendations_list", __name__)


@recommendations_blueprint.route('/recommendations_list', methods=["GET", "POST"])
@jwt_required()
def handle_movies():
    if request.method == "POST": return create()
    if request.method == "GET": return index()


@recommendations_blueprint.route('/recommendations_list/<int:id>', methods=["GET", "PATCH", "DELETE"])
@jwt_required()
def handle_movie_list(id):
    if request.method == "GET": return show(id)
    if request.method == "PATCH": return update(id)
    if request.method == "DELETE": return destroy(id)


@recommendations_blueprint.route('/recommendations_list_manage/<int:id>/<int:movie_id>', methods=["GET", "PATCH", "DELETE"])
@jwt_required()
def handle_movie(id,movie_id):
    if request.method == "GET": return show_movie_details(id,movie_id)
    if request.method == "PATCH": return add_movie(id,movie_id)
    if request.method == "DELETE": return remove_movie(id,movie_id)


@recommendations_blueprint.route('/recommendations_list_recommend/<int:id>', methods=["PATCH"])
@jwt_required()
def recommend_movie(id):
    if request.method == "PATCH": return recommend(id)


@recommendations_blueprint.errorhandler(exceptions.NotFound)
def handle_404(err):
    return { "error": f"Oops {err}"}, 404


@recommendations_blueprint.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return { "error": f"Oops {err} "}, 500


@recommendations_blueprint.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return { "error": f"Oops {err}" }, 400


# Route for a full-text searching of a movie to give the user an option add movies manually
@recommendations_blueprint.route('/search', methods=['POST'])
@jwt_required()
def handle_search():
    return search()
