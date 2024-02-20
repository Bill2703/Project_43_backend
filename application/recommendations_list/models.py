from application import db


class RecommendationsList(db.Model):
    __tablename__ = 'recommendations_list'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    # movie_ids=db.Column(db.ARRAY(db.Integer))
    movie_ids = db.Column(db.String(2000))
    title = db.Column(db.String(500), nullable=False)

    def __init__(self, user_id, title, movie_ids):
        self.user_id = user_id
        self.title = title
        self.movie_ids = movie_ids

    def __repr__(self):
        return f"Movie (id:{self.id},movie_ids:{self.movie_ids},user_id:{self.user_id} title:{self.title})"

    @property
    def json(self):
        return {"id": self.id, "user_id": self.user_id, "movie_ids": self.movie_ids, "title": self.title}
