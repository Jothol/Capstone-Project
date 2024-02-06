import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

membership = sp.current_user()["product"]
print(membership)

