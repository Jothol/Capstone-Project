import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing user-read-recently-played user-library-read streaming user-modify-playback-state"

# note: redirect URI needs to have a port and be http, not https
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_recently_played(limit=20)
print("Test: User's Recently Played")
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx+1, ": ", track['artists'][0]['name'], " - ", track['name'])
