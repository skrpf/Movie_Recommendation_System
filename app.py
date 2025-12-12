from abc import ABC, abstractmethod
import requests
import pickle
import concurrent.futures
import streamlit as st
import base64

class IPosterProvider(ABC):
    @abstractmethod
    def get_poster_url(self, movie_id):
        pass


# --- CONCRETE IMPLEMENTATION (Single Responsibility: Network I/O) ---
class TMDBPosterProvider(IPosterProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3/movie/"
        self.image_base = "https://image.tmdb.org/t/p/w500/"

    def get_poster_url(self, movie_id):
        try:
            url = f"{self.base_url}{movie_id}?api_key={self.api_key}&language=en-US"
            # Timeout is crucial for network resilience
            response = requests.get(url, timeout=2)
            data = response.json()
            path = data.get('poster_path')
            if path:
                return self.image_base + path
        except Exception:
            pass
        # Fallback image if API fails
        return "https://via.placeholder.com/500x750?text=No+Image"


# --- BUSINESS LOGIC (Single Responsibility: Math/ML) ---
class MovieRecommender:
    def __init__(self, movie_file, similarity_file, poster_provider: IPosterProvider):
        self.movies = pickle.load(open(movie_file, 'rb'))
        self.similarity = pickle.load(open(similarity_file, 'rb'))
        self.poster_provider = poster_provider

    def get_recommendations(self, movie_name):
        # 1. Logic: Find the movie index
        try:
            idx = self.movies[self.movies['title'] == movie_name].index[0]
        except IndexError:
            return [], []

        # 2. Logic: Calculate Similarity
        distances = sorted(list(enumerate(self.similarity[idx])), reverse=True, key=lambda x: x[1])
        top_indices = [i[0] for i in distances[1:6]]

        # 3. Data Extraction
        names = self.movies.iloc[top_indices]['title'].tolist()
        movie_ids = self.movies.iloc[top_indices]['movie_id'].tolist()

        # 4. Delegation: Ask the provider for images (Parallelized for speed)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            posters = list(executor.map(self.poster_provider.get_poster_url, movie_ids))

        return names, posters

    def get_movie_list(self):
        return self.movies['title'].values


# ==========================================
# 2. STREAMLIT UI & CONFIGURATION
# ==========================================

# --- CONFIGURATION ---
API_KEY = "85bba7cbb6e6274542b0a71c84778c94"


# --- HELPER: BACKGROUND IMAGE ---
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read())

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"Background image '{image_file}' not found. Using default background.")


# --- COMPOSITION ROOT (Setup) ---
@st.cache_resource
def get_engine():
    # 1. Create the specific poster service
    poster_service = TMDBPosterProvider(API_KEY)

    # 2. Inject dependencies
    return MovieRecommender('movie_list.pkl', 'similarity.pkl', poster_service)


# Initialize Engine
try:
    engine = get_engine()
except FileNotFoundError:
    st.error("Critical Error: 'movie_list.pkl' or 'similarity.pkl' not found.")
    st.stop()

# ==========================================
# 3. RENDER UI
# ==========================================

# --- APPLY BACKGROUND ---
# REPLACE 'background.jpg' with your actual image filename!
add_bg_from_local('background.jpg')

# --- MAIN APP ---
st.header('Movies to Watch')

selected_movie = st.selectbox(
    "Type or select a movie",
    engine.get_movie_list()
)

if st.button('Recommendation'):
    names, posters = engine.get_recommendations(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
