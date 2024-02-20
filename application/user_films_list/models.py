from .. import db

class UserFilmList(db.Model):
    __tablename__ = "user_film_lists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    
    def __init__(self, user_id, movies_id):
        self.user_id = user_id
        self.movies_id = movies_id
