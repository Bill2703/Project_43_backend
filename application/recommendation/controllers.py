import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import g
from .. import db

def get_model():
    if 'model' not in g:
        g.model = train_model()
    return g.model


def load_movie_dataset():
    if 'movie_dataset' not in g:
        g.movie_dataset = pd.read_sql(sql='movies_dataset', con=db.engine)
        g.movie_dataset.set_index('index', inplace=True, drop=False)


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


def train_model():
    load_movie_dataset()
    features = ['keywords', 'cast', 'genres', 'director']

    def combine_features(row):
        return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]

    for feature in features:
        g.movie_dataset[feature] = g.movie_dataset[feature].fillna('')
    g.movie_dataset["combined_features"] = g.movie_dataset.apply(combine_features, axis=1)
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(g.movie_dataset["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)
    print("train model")
    return cosine_sim


def recommend_movie(movie_ids):
    #doing the list from movie_ids
    list_of_movie_ids=movie_ids.split(";")
    if (list_of_movie_ids[0]==''):
        return -1
    list_of_movie_ids = [int(movie_id) for movie_id in list_of_movie_ids[:-1]] #make the list integer
    dictionary_of_similar_movies=dict()

    for movie_id in list_of_movie_ids:
        similar_movies = list(enumerate(get_model()[movie_id]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

        i = 0
        for element in sorted_similar_movies:
            dictionary_of_similar_movies[element[0]] = dictionary_of_similar_movies.get(element[0], 0) + 1
            i = i + 1
            if i >= 5:
                break
     #Remove from dictionary_of_similar_movies all entries with keys from list_of_movie_ids
    dictionary_of_similar_movies = {key: value for key, value in dictionary_of_similar_movies.items() if key not in list_of_movie_ids}
    
    return max(dictionary_of_similar_movies, key=dictionary_of_similar_movies.get)
