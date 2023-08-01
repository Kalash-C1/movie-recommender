import pandas as pd
import ast
import os
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

file_path = os.path.join(os.path.dirname(__file__), 'tmdb_5000_movies.csv')

movies = pd.read_csv(file_path)
movies = movies[['id', 'title', 'overview', 'genres', 'keywords']]
movies = movies.dropna()

def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

def preprocess_text(text):
    return [word.replace(" ", "") for word in text]

movies['genres'] = movies['genres'].apply(convert)
movies['genres'] = movies['genres'].apply(preprocess_text)
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['overview'] = movies['overview'].apply(preprocess_text)
movies['keywords'] = movies['keywords'].apply(convert)
movies['keywords'] = movies['keywords'].apply(preprocess_text)
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords']
new_movies = movies[['id', 'title', 'tags']]
new_movies['tags'] = new_movies['tags'].apply(lambda x: " ".join(x))
new_movies['tags'] = new_movies['tags'].apply(lambda x: x.lower())

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_movies['tags']).toarray()

ps = PorterStemmer()
new_movies['tags'] = new_movies['tags'].apply(lambda x: " ".join([ps.stem(word) for word in x.split()]))

similarity = cosine_similarity(vectors)

def recommend(movie):
    try:
        movie_index = new_movies[new_movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommendations=[]
        for i in movie_list:
            recommendations.append(new_movies.iloc[i[0]].title)
        return recommendations
    except IndexError:
        return []
