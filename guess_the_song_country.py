import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

client_id = '3031844aaf224c56926b3dc24b5fda23'
client_secret = '14054d67e4824df9b08144aea8738263'

# Check if environment variables are set
if not client_id or not client_secret:
    st.error("Spotify API credentials are not set. Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.")
    st.stop()

# Authenticate with Spotify API
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
except spotipy.oauth2.SpotifyOauthError as e:
    st.error("Spotify authentication failed. Check your API credentials.")
    st.stop()

# Fetch playlist
playlist_id = '0fyny8Z9OQStqf4VGjK9Np'
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# Function to get a random track
def get_random_track(tracks):
    track = random.choice(tracks)['track']
    return track

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
