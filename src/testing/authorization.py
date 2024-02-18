import spotipy
from spotipy.oauth2 import SpotifyOAuth

<<<<<<< HEAD
scope = "user-read-currently-playing user-read-recently-played user-library-read streaming user-modify-playback-state"
=======
scope = (
    "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public "
    "user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read"
    "user-follow-modify user-follow-read")
>>>>>>> d45b0541f06be408e70f54b3746aa19ac9a8340a

# note: redirect URI needs to have a port and be http, not https
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

<<<<<<< HEAD
results = sp.current_user_recently_played(limit=20)
print("Test: User's Recently Played")
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx+1, ": ", track['artists'][0]['name'], " - ", track['name'])
=======
results = sp.current_user_followed_artists(limit=20)
print(results)
print("Test: User's Recently Played")
for idx, item in enumerate(results['items']):
    track = item['track']
    print(track)
    print(idx + 1, ": ", track['artists'][0]['name'], " - ", track['name'])
>>>>>>> d45b0541f06be408e70f54b3746aa19ac9a8340a
