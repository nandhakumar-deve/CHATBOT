import requests
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# TMDb API key (Replace with your actual key)
TMDB_API_KEY = "edf864e42ce96dcb08df176c0ba7bb2c"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Define the Movie data structure
class Message(BaseModel):
    message: str

def get_movies_by_genre(genre: str):
    # TMDb endpoint for getting movies by genre
    genre_ids = {
        'comedy': 35,
        'sci-fi': 878,
        'action': 28,
        'romance': 10749   # <-- added romance!
    }

    genre_id = genre_ids.get(genre)
    if not genre_id:
        return []

    # Make a GET request to TMDb API
    headers = {"Authorization": f"Bearer {TMDB_API_KEY}"}
    url = f"{TMDB_BASE_URL}/discover/movie?with_genres={genre_id}&language=en-US"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    # Extract movie titles from the response
    movies = response.json().get('results', [])
    return [movie['title'] for movie in movies]

@app.post("/recommend")
async def recommend_movie(msg: Message):
    mood = msg.message.lower()

    # Determine the genre from the message
    if 'comedy' in mood:
        genre = 'comedy'
    elif 'sci-fi' in mood:
        genre = 'sci-fi'
    elif 'action' in mood:
        genre = 'action'
    elif 'romance' in mood:    # <-- added romance!
        genre = 'romance'
    else:
        genre = random.choice(['comedy', 'sci-fi', 'action', 'romance'])  

    # Fetch movies from TMDb API based on the genre
    movies = get_movies_by_genre(genre)

    if not movies:
        return {"response": f"Sorry, I couldn't find any {genre} movies right now!"}

    # Select a random movie from the fetched list
    recommended_movie = random.choice(movies)
    return {"response": f"How about watching '{recommended_movie}'? It's a great {genre} movie!"}

@app.post("/clear")
async def clear_history():
    return {"response": "Chat history cleared!"}
