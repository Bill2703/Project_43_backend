from .. import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

movie_genre_association = db.Table(
    'movie_genre_association',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    original_language = db.Column(db.String(3), nullable=False)
    original_title = db.Column(db.String(300), nullable=False)
    overview = db.Column(db.String(1000), nullable=False)
    vote_average = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    poster_path = db.Column(db.String(200), nullable=True)
    genre_ids = db.Column(ARRAY(db.Integer), nullable=True)
     # Define the many-to-many relationship
    genres = db.relationship('Genre', secondary=movie_genre_association, backref='movies')



    def __init__(self, original_title, original_language, overview, vote_average, release_date, poster_path, genre_ids): # constructor
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.vote_average = vote_average
        self.release_date = release_date
        self.poster_path = poster_path
        self.genre_ids = genre_ids


    def __repr__(self):
        return f"Movie(id:  {self.id}, name: {self.original_title})"
    
    @property
    def poster_url(self):
        base_url = "https://image.tmdb.org/t/p/w500"
        return f"{base_url}{self.poster_path}" if self.poster_path else None
    
    @property
    def genres(self):
        movie_genres = []
        for id in self.genre_ids:
            genre = Genre.query.get(id).name
            movie_genres.append(genre)
        return movie_genres

    @property
    def json(self): # create a json from of an instance
        return {
            "id": self.id,
            "original_title": self.original_title,
            "original_language": self.original_language,
            "overview": self.overview,
            "vote_average": self.vote_average,
            "release_date": self.release_date,
            "poster_path": self.poster_path,
            "genres": self.genres
        }


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


    def __init__(self, id, name): # constructor
        self.id = id
        self.name = name       
        

    def __repr__(self):
        return f"Genre(id:  {self.id}, api_id: {self.api_id}, name: {self.name})"

    @property
    def json(self): # create a json from of an instance
        return {
            "id": self.id,
            "name": self.name
        }
    
 

