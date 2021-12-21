import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    dinstance = similarity[movie_index]
    movie_list = sorted(list(enumerate(dinstance)),reverse = True, key=lambda x:x[1])[1:6] #updated distance
    #we got movie list lets print all 5
    recommended = []
    recommended_poster = []
    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_poster.append(fetch_poster(movie_id )) #fetch poster from API and appended to list
        recommended.append(movies_df.iloc[i[0]].title)
    return recommended, recommended_poster

movies_pkl = pickle.load(open('movies.pkl', 'rb'))
movies_df = pd.DataFrame(movies_pkl)

st.title('Movie Recommender System')
option = st.selectbox('Please Select Movie Name Over Here', movies_df['title'].values)
if st.button('Recommended'):
    recommendation, poster = recommend(option)
    #for i in recommendation:
        #st.write(i)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendation[0])
        st.image(poster[0])
    with col2:
        st.text(recommendation[1])
        st.image(poster[1])
    with col3:
        st.text(recommendation[2])
        st.image(poster[2])
    with col4:
        st.text(recommendation[3])
        st.image(poster[3])
    with col5:
        st.text(recommendation[4])
        st.image(poster[4])
