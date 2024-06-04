import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Spotify API credentials
client_id = '3031844aaf224c56926b3dc24b5fda23'
client_secret = 'c6d0671d773d437ab7a6eb1232ca01fc'

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Fetch playlist
playlist_id = '0fyny8Z9OQStqf4VGjK9Np'
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# Function to get a random track
def get_random_track(tracks):
    track = random.choice(tracks)['track']
    return track

# Streamlit app
st.title("Guess the Country of Origin")

# Get a random track
track = get_random_track(tracks)
track_name = track['name']
track_preview_url = track['preview_url']
track_artist = track['artists'][0]['name']

# Display track info
st.write(f"Track: {track_name} by {track_artist}")

# Play 30-second sample
if track_preview_url:
    st.audio(track_preview_url, format="audio/mp3")
else:
    st.write("No preview available for this track.")

# Options for the user to guess
countries = ['Country 1', 'Country 2', 'Country 3', 'Country 4']  # Replace with actual country names
correct_country = 'Country 1'  # Replace with actual country of origin

# User guess
user_guess = st.radio("Guess the country of origin", countries)

# Check guess
if st.button("Submit"):
    if user_guess == correct_country:
        st.success("Correct!")
    else:
        st.error("Incorrect! The correct answer is " + correct_country)

# Track performance
if 'score' not in st.session_state:
    st.session_state.score = 0

if st.button("Next Track"):
    if user_guess == correct_country:
        st.session_state.score += 1
    st.write(f"Score: {st.session_state.score}")
