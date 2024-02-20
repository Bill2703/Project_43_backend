import pandas as pd
from sqlalchemy import text
from application import db,create_app
from application.auth.models import User
from application.movies.controller import index_and_seed, genres_and_seed
from application.reviews.models import Reviews
from application.user_films_list.models import UserFilmList


app = create_app("PROD")
db.drop_all()
# db.session.execute(text('DROP TABLE IF EXISTS genres;'))
# db.session.execute(text('DROP TABLE IF EXISTS user_film_lists;'))
# db.session.execute(text('DROP TABLE IF EXISTS reviews;'))
# db.session.execute(text('DROP TABLE IF EXISTS movies;'))

print("Dropping Database")

result = db.session.execute(text('DROP TABLE IF EXISTS movies_dataset;'))

db.session.commit()



db.create_all()
print("Creating database")

print("Saving movies")
index_and_seed()

print("Saving genres")
genres_and_seed()

print("Saving movies dataset")
df = pd.read_csv("../movie_dataset.csv")
df.to_sql(name='movies_dataset', con=db.engine)
print("movies dataset saved")

user_list_data = [
    {"user_id": 1, "movies_id": 2},
    {"user_id": 2, "movies_id": 199}
]

for list_info in user_list_data:
    list = UserFilmList(**list_info)
    db.session.add(list)



user_data = [
    {"email": "test@test.com", "password": "test", "name": "test"},
    {"email": "test2@test.com", "password": "test2", "name": "test2"}
]

for user_info in user_data:
    user = User(**user_info)
    db.session.add(user)

# Seed reviews data
print("Saving reviews")
# Manually create some review records and insert them into the 'reviews' table
reviews_data = [
    {"title": "Great Movie", "content": "I loved it!", "rating": 5, "user_id": 1, "movies_id": 1},
    {"title": "Average Movie", "content": "It was okay", "rating": 3, "user_id": 2, "movies_id": 2},
]

for review_info in reviews_data:
    review = Reviews(**review_info)
    db.session.add(review)


db.session.commit()
print("commit")
