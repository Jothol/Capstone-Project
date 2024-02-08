import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = ("user-read-playback-state user-modify-playback-state user-read-currently-playing streaming "
         "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public "
         "user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played "
         "user-library-modify user-library-read user-read-email user-read-private")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

membership = sp.current_user()["product"]
if membership != "premium":
    print("You are not authorized to access this")
else:
    results = sp.current_user_recently_played(limit=1)
    artist_uri = [(results["items"][0]["track"]["artists"][0]["uri"]).split(":", 3)[2]]
    track_uri = [(results["items"][0]["track"]["uri"]).split(":", 3)[2]]
    artistinfo = sp.artist(artist_uri[0])
    genres = artistinfo["genres"]
    rec = sp.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, seed_genres=[genres[0]], limit=1)
    print(rec["tracks"][0]["album"]["images"][0]["url"])
    print(rec["tracks"][0]["artists"][0]["name"])
    print(rec["tracks"][0]["name"])


