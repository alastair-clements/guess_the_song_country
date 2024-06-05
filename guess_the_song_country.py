import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import random
import folium
from folium.plugins import ClickForMarker
from geopy.distance import geodesic
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

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

# Function to create a map with click functionality
def create_map():
    m = folium.Map(location=[20, 0], zoom_start=2)
    ClickForMarker().add_to(m)
    return m

# Function to get the coordinates of a country
def get_country_coordinates(country):
    # Replace with actual country coordinates
    country_coords = {
        "Country 1": (10, 20),
        "Country 2": (30, 40),
        "Country 3": (50, 60),
        "Country 4": (70, 80)
    }
    return country_coords.get(country, (0, 0))

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

# Display map
st.write("Click on the map to guess the country of origin")
map_ = create_map()
components.html(folium.Map()._repr_html_(), height=600)

# Get user's guess
user_lat = st.number_input("Latitude", value=0.0)
user_lon = st.number_input("Longitude", value=0.0)

# Correct country (replace with actual logic)
correct_country = "Country 1"
correct_coords = get_country_coordinates(correct_country)

# Calculate distance between user's guess and correct country
user_coords = (user_lat, user_lon)
distance = geodesic(user_coords, correct_coords).kilometers

# Check guess
if st.button("Submit"):
    st.write(f"Your guess is {distance:.2f} km away from the correct country.")
    if distance < 500:  # Adjust the threshold as needed
        st.success("Correct!")
    else:
        st.error("Incorrect! The correct country is " + correct_country)

# Track performance
if 'score' not in st.session_state:
    st.session_state.score = 0

if st.button("Next Track"):
    if distance < 500:  # Adjust the threshold as needed
        st.session_state.score += 1
    st.write(f"Score: {st.session_state.score}")
