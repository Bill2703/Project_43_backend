from .. import db
from datetime import datetime

class Reviews(db.Model):
    __tablename__='reviews'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Title = db.Column(db.String(100), unique=True)
    Content = db.Column(db.String(500))
    Timestamp = db.Column(db.DateTime)
    Rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

    def __init__(self, title, content, rating, user_id, movies_id):
        self.Title = title
        self.Content = content
        self.Rating = rating
        self.user_id = user_id
        self.movies_id = movies_id
        self.Timestamp = datetime.utcnow()

    def serialize(self):
        return {
            'id': self.id,
            'Title': self.Title,
            'Content': self.Content,
            'Timestamp': self.Timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Rating': self.Rating,
            'user_id': self.user_id,
            'movies_id': self.movies_id
        }

db.Index('reviews_unique_title', Reviews.Title, unique=True)
db.ForeignKeyConstraint(['movies_id'], ['movies.id'])

