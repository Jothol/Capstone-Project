from random import random

import spotipy
from spotipy import SpotifyPKCE

scope = ("user-read-playback-state user-modify-playback-state user-read-currently-playing streaming "
         "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public "
         "user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played "
         "user-library-modify user-library-read user-read-email user-read-private")
SPOTIPY_CLIENT_ID = '66880bb5822a48459696468e620a10d6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080'


def spotify_rec_with_keys(track, features):
    auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth)
    membership = sp.current_user()["product"]
    if membership != "premium":
        print("You are not authorized to access this")
    else:
        results = sp.search(q="track:" + track, type="track")
        artist_uri = [(results["tracks"]["items"][0]["artists"][0]["uri"]).split(":", 3)[2]]
        track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
        artistinfo = sp.artist(artist_uri[0])
        genres = artistinfo["genres"]
        rec = sp.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, seed_genres=[genres[0]], limit=10,
                                 target_danceability=features["danceability"], target_energy=features["energy"],
                                 target_valence=features["valence"])
        sp.add_to_queue(rec["tracks"][0]["uri"])
        return rec["tracks"][0]["name"]


def get_features(track):
    auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth)
    membership = sp.current_user()["product"]
    if membership != "premium":
        print("You are not authorized to access this")
    else:
        results = sp.search(q="track:" + track, type="track")
        track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
        features = sp.audio_features(track_uri)
        return features


def balanceValues(features, likes, dislikes):
    new_features = {"danceability": features["danceability"], "energy": features["energy"],
                    "valence": features["valence"]}
    difference = ((dislikes - likes)/(likes + dislikes))/10
    if difference == 0:
        if random() > 0.5:
            difference = 0.05
        else:
            difference = -0.05
    new_features["danceability"] = max(1, min(0, round(features["danceability"]+difference, 3)))
    new_features["energy"] = max(1, min(0, round(features["energy"]+difference, 3)))
    new_features["valence"] = max(1, min(0, round(features["valence"]+difference, 3)))
    return new_features


song_name = "Let It Be"

input = get_features(song_name)[0]
features = {"danceability": input["danceability"], "energy": input["energy"], "valence": input["valence"]}
likes = 7
dislikes = 4
features = balanceValues(features, likes, dislikes)
next_song = (spotify_rec_with_keys(song_name, features))
input = get_features(next_song)[0]
features = {"danceability": input["danceability"], "energy": input["energy"], "valence": input["valence"]}
likes = 8
dislikes = 60
features = balanceValues(features, likes, dislikes)
next = spotify_rec_with_keys(next_song, features)

"""Want to focus on 
    danceability 0(least danceable) - 1(most danceable)
    energy 0(think bach) - 1(think heavy metal)
    valence 0(think sad)-1(think happy)
"""
