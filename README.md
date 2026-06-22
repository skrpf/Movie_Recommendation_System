# 🎬 Movie Recommendation System
 
A content-based movie recommendation system built with Python and Streamlit. Select any movie and instantly get 5 similar recommendations with posters, powered by cosine similarity on TMDB metadata.
 
![App Screenshot](screenshot.png)
 
---
 
## 🧠 How It Works
 
1. Movie metadata (genres, cast, crew, keywords, and overview) is combined into a single "tags" vector for each movie.
2. These tags are vectorized using **CountVectorizer**.
3. **Cosine similarity** is computed between all movie vectors.
4. When you select a movie, the system finds the 5 most similar movies based on that similarity score.
5. Movie posters are fetched in real-time from the **TMDB API** using multithreading for speed.
---
 
## 🗂️ Dataset
 
[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle.
 
Download both files:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`
---
 
## 🛠️ Tech Stack
 
| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| scikit-learn | CountVectorizer + cosine similarity |
| pandas | Data processing |
| requests | TMDB API calls |
| TMDB API | Fetching movie posters |
 
---
 
## 📁 Project Structure
 
```
Movie_Recommendation_System/
│
├── app.py                        # Streamlit app (UI + recommendation logic)
├── notebook86c26b4f17.ipynb      # Data preprocessing + model building
├── movie_list.pkl                # Preprocessed movie data (title + movie_id)
├── similarity.pkl                # Cosine similarity matrix (generate from notebook)
├── background.jpg                # Background image for the app
├── requirements.txt              # Python dependencies
└── README.md
```
 
---
 
## ⚙️ Setup & Installation
 
### 1. Clone the repository
```bash
git clone https://github.com/skrpf/Movie_Recommendation_System.git
cd Movie_Recommendation_System
```
 
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
 
### 3. Set up your TMDB API Key
 
Get a free API key from [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api).
 
Create a `.env` file in the root folder:
```
TMDB_API_KEY=your_api_key_here
```
 
### 4. Generate the model files
 
Download the dataset from Kaggle (see above), place both CSV files in the project root, then run the notebook:
```bash
jupyter notebook notebook86c26b4f17.ipynb
```
 
Run all cells — this will generate `movie_list.pkl` and `similarity.pkl`.
 
### 5. Run the app
```bash
streamlit run app.py
```
 
Open `http://localhost:8501` in your browser.
 
---
 
## 🖥️ Usage
 
1. Select or type a movie name in the dropdown.
2. Click **Get Recommendations**.
3. View 5 similar movies with their posters.
---
 
## 📦 Requirements
 
```
streamlit
requests
scikit-learn
pandas
numpy
```
 
Or install from `requirements.txt`:
```bash
pip install -r requirements.txt
```
 
---
 
## ⚠️ Known Limitations
 
- Recommendations are based only on metadata (genre, cast, crew, keywords) — not user ratings or viewing history.
- Poster fetching depends on TMDB API availability. If the API is down, a placeholder image is shown.
- The similarity matrix (`similarity.pkl`) can be large (~100MB+) and is not included in the repo — you need to generate it from the notebook.
---
 
## 🙌 Acknowledgements
 
- [TMDB](https://www.themoviedb.org/) for the movie data and poster API.
- [Kaggle - TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
 
<img width="1909" height="1006" alt="Image" src="https://github.com/user-attachments/assets/d953b1e0-d152-40ab-9b3d-60d871158c76" />
