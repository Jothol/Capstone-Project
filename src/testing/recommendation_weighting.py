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
    new_features = {"danceability": features["danceability"], "energy": features["energy"], "valence": features["valence"]}
    total = likes + dislikes
    like_per = 100 * likes / total
    dislike_per = 100 * dislikes / total
    difference = like_per - dislike_per
    if difference >= 50:
        new_features["danceability"] = min(1, features["danceability"] + like_per*0.006)
        new_features["energy"] = min(1, features["energy"] + like_per * 0.006)
        new_features["valence"] = min(1, features["valence"] + like_per * 0.006)
    elif 50 > difference >= 40:
        new_features["danceability"] = min(1, features["danceability"] + like_per * 0.005)
        new_features["energy"] = min(1, features["energy"] + like_per * 0.005)
        new_features["valence"] = min(1, features["valence"] + like_per * 0.005)
    elif 40 > difference >= 30:
        new_features["danceability"] = min(1, features["danceability"] + like_per * 0.004)
        new_features["energy"] = min(1, features["energy"] + like_per * 0.004)
        new_features["valence"] = min(1, features["valence"] + like_per * 0.004)
    elif 30 > difference >= 20:
        new_features["danceability"] = min(1, features["danceability"] + like_per * 0.003)
        new_features["energy"] = min(1, features["energy"] + like_per * 0.003)
        new_features["valence"] = min(1, features["valence"] + like_per * 0.003)
    elif 20 > difference >= 10:
        new_features["danceability"] = min(1, features["danceability"] + like_per * 0.002)
        new_features["energy"] = min(1, features["energy"] + like_per * 0.002)
        new_features["valence"] = min(1, features["valence"] + like_per * 0.002)
    elif 10 > difference > 0:
        new_features["danceability"] = min(1, features["danceability"] + like_per * 0.001)
        new_features["energy"] = min(1, features["energy"] + like_per * 0.001)
        new_features["valence"] = min(1, features["valence"] + like_per * 0.001)
    elif difference == 0:
        new_features["danceability"] = features["danceability"]
        new_features["energy"] = features["energy"]
        new_features["valence"] = features["valence"]
    elif 0 > difference >= -10:
        new_features["danceability"] = max(0, features["danceability"] - dislike_per * 0.001)
        new_features["energy"] = max(0, features["energy"] - dislike_per * 0.001)
        new_features["valence"] = max(0, features["valence"] - dislike_per * 0.001)
    elif -10 > difference >= -20:
        new_features["danceability"] = max(0, features["danceability"] - dislike_per * 0.002)
        new_features["energy"] = max(0, features["energy"] - dislike_per * 0.002)
        new_features["valence"] = max(0, features["valence"] - dislike_per * 0.002)
    elif -20 > difference >= -30:
        new_features["danceability"] = max(0, features["danceability"] - dislike_per * 0.003)
        new_features["energy"] = max(0, features["energy"] - dislike_per * 0.003)
        new_features["valence"] = max(0, features["valence"] - dislike_per * 0.003)
    elif -30 > difference >= -40:
        new_features["danceability"] = max(0, features["danceability"] - dislike_per * 0.004)
        new_features["energy"] = max(0, features["energy"] - dislike_per * 0.004)
        new_features["valence"] = max(0, features["valence"] - dislike_per * 0.004)
    elif -40 > difference >= -50:
        new_features["danceability"] = max(0, features["danceability"] - dislike_per * 0.005)
        new_features["energy"] = max(0, features["energy"] - dislike_per * 0.005)
        new_features["valence"] = max(0, features["valence"] - dislike_per * 0.005)
    elif difference < -50:
        new_features["danceability"] = max(0, features["danceability"] - dislike_per * 0.006)
        new_features["energy"] = max(0, features["energy"] - dislike_per * 0.006)
        new_features["valence"] = max(0, features["valence"] - dislike_per * 0.006)
    new_features["danceability"] = round(new_features["danceability"], 3)
    new_features["energy"] = round(new_features["energy"], 3)
    new_features["valence"] = round(new_features["valence"], 3)
    return new_features

#print(get_features("Little Lion Man"))
features = {"danceability": 0.9, "energy": 0.5, "valence": 0.4}
next_song = (spotify_rec_with_keys("Little Lion Man", features))

likes = 7
dislikes = 4

next = spotify_rec_with_keys(next_song, balanceValues(features, likes, dislikes))

"""Want to focus on 
    danceability 0(least danceable) - 1(most danceable)
    energy 0(think bach) - 1(think heavy metal)
    valence 0(think sad)-1(think happy)
"""