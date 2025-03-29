import streamlit as st
import pickle
import pandas as pd
import requests
import os
from pathlib import Path


# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    API_KEY = "5cde0d830dfefdf348875fafe2dafccc"  # This should ideally be moved to env variables
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None  # Return None if poster not found
    except (requests.exceptions.RequestException, ValueError) as e:
        st.warning(f"Could not fetch poster for movie ID {movie_id}: {str(e)}")
        return None


# Load Movies Data with error handling
@st.cache_data  # Cache the data loading
def load_data():
    try:
        # Check if files exist
        if not Path('movies.pkl').exists():
            st.error("Movies data file not found. Please check that 'movies.pkl' exists in the app directory.")
            return None, None
        if not Path('similarity.pkl').exists():
            st.error(
                "Similarity matrix file not found. Please check that 'similarity.pkl' exists in the app directory.")
            return None, None

        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


movies, similarity = load_data()

st.title('🎬 Movie Recommendation System')

# Only show the select box if data is loaded successfully
if movies is not None:
    # Select movie
    selected_movie_name = st.selectbox(
        "Select a movie to get recommendations:",
        movies['title'].values
    )


    # Recommendation Function
    def recommend(movie):
        try:
            # Check if movie exists in our dataset
            if movie not in movies['title'].values:
                return ["Movie not found in database"], []

            movie_index = movies[movies['title'] == movie].index[0]

            # Check if index is within range of similarity matrix
            if movie_index >= len(similarity):
                return ["Similarity data not available for this movie"], []

            distances = similarity[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

            recommended_movies = []
            recommended_posters = []

            for i in movies_list:
                try:
                    # Make sure index is within range
                    if i[0] < len(movies):
                        # Convert movie_id to integer if needed
                        movie_id = movies.iloc[i[0]].movie_id
                        if movie_id is not None:  # Check if movie_id is available
                            recommended_movies.append(movies.iloc[i[0]].title)
                            recommended_posters.append(fetch_poster(movie_id))
                except Exception as e:
                    st.warning(f"Error processing recommendation: {str(e)}")
                    continue

            # If no recommendations were successfully processed
            if not recommended_movies:
                return ["Could not generate recommendations"], []

            return recommended_movies, recommended_posters
        except IndexError:
            return ["No recommendations available"], []
        except Exception as e:
            st.error(f"Recommendation error: {str(e)}")
            return ["Error generating recommendations"], []


    # Button to Show Recommendations
    if st.button('Recommend'):
        recommendations, posters = recommend(selected_movie_name)

        st.subheader("🎥 Recommended Movies:")

        # Display movie posters along with titles
        for i in range(len(recommendations)):
            col1, col2 = st.columns([1, 3])  # Create two columns
            with col1:
                if i < len(posters) and posters[i]:  # Show poster if available
                    st.image(posters[i], width=120)
                else:
                    st.write("🖼️ No poster available")
            with col2:
                st.write(f"🎬 {recommendations[i]}")
else:
    st.error("Could not start the recommendation system due to missing data. Please check the application logs.")