
import os
import streamlit as st
import pandas as pd
st.title("🎬 Movie Recommendation System")
st.write("Welcome! Select a movie from the dropdown to get recommendations.")
#update the frontend to display posters along with movie names
if not os.path.exists('similarity.pkl'):
    url="https://drive.google.com/file/d/1jYO7rw49NHfWrYQHqIN1_mJz_YduAK6i/view"
    gdown.download(url,'similarity.pkl',quiet=False)
similarity = pickle.load(open('similarity.pkl', 'rb'))

from dotenv import load_dotenv
import pickle 
import requests
load_dotenv()
api_key = os.getenv('TMDB_API_KEY')
def fetch_poster(movie_id):
    try:
        url =  f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
        
        
    except Exception as e:
        st.warning(f"Poster not found for movie ID {movie_id}. Using placeholder.")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

def recommend(movie):
    if 'movie_id' not in movies.columns:
        st.error("❌ 'movie_id' column missing in the movies dataset.")
        return [], []
    movie_index=movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommend_movies=[]
    recommend_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies ,recommend_movies_posters


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


movie_list=pickle.load(open('movies.pkl','rb'))
movie_list=movie_list['title'].values

selected_movie_name=st.selectbox("Select a movie",movies['title'].values)
if st.button('Recommend'):
    names,posters =recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])  
