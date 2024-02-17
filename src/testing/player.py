import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = (
    "user-read-currently-playing " 
    "user-read-recently-played " 
    "user-library-read " 
    "streaming "
    "user-modify-playback-state "
    "user-read-private ")

# note: redirect URI needs to have a port and be http, not https
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

membership = sp.current_user()["product"]
keepLooping = 1
choice = 0

if membership != "premium":
    print("You are not authorized to access this")
else:
    while keepLooping == 1:
        choice = int(input('Options! Press 1 to pause, press 2 to play, press any other key to exit.'))
        if choice == 1:
            sp.pause_playback()
        elif choice == 2:
            sp.start_playback()
        else:
            exit(0)
