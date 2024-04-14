from datetime import datetime
from random import random

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyPKCE

scope = (
    "user-read-currently-playing "
    "user-read-recently-played "
    "user-library-read "
    "streaming "
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-private "
    "playlist-modify-public "
    "playlist-modify-private "
)

SPOTIPY_CLIENT_ID = '66880bb5822a48459696468e620a10d6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080'

di = "unselected"
dv = -1


# @author Serenity
# use this function to get information out of a track uri - least headaches this way
def get_data_from_track_uri(uri):
    try:
        track = sp.track(uri)
        # image = track["album"]["images"][0]["url"]
        artist_name = track["artists"][0]["name"]
        track_name = track["name"]
        return {"artist_name": artist_name, "track_name": track_name}
    except SpotifyException as err:
        print("Error in get_data_from_track_uri:", err)


def queue_song(sp_client, uri):
    try:
        sp_client.add_to_queue(uri)
        # this is going to be interesting - the session history is shared across users, sp is local to each user.
        # maybe solution should be to give this a list of each user's sp's to add to each queue individually?
        session_history.append(uri)
    except SpotifyException as err:
        print("Error in enqueue:", err)


def make_playlist_from_history(sp_client):
    user_id = sp_client.current_user()["id"]
    date_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    playlist = sp_client.user_playlist_create(user=user_id, name=date_string, description="Created by Spotivibe.")["id"]
    sp_client.user_playlist_add_tracks(user=user_id, playlist_id=playlist, tracks=session_history)


def play_button_functionality(sp_client, listening_device, session=None):
    try:
        currently_playing = sp_client.currently_playing()
        print(currently_playing)
        if session is not None and session.get_uri() != "" and session.get_uri() != currently_playing["item"]["uri"]:
            queue_song(sp_client, session.get_uri())
            sp_client.next_track()
        if currently_playing is None:
            print("No track playing. Greyed out play button.")
        elif currently_playing["is_playing"] is False:
            sp_client.start_playback(device_id=listening_device)
        elif currently_playing["is_playing"] is True:
            sp_client.pause_playback(device_id=listening_device)
    except SpotifyException as err:
        print("Error in play button:", err)


def volume_functionality(sp_client, volume):
    vol = int(volume)
    try:
        if 0 <= vol <= 100:
            # do this for now,
            sp_client.volume(vol)
        else:
            print("Invalid volume percentage number. Ignore volume set")
    except ValueError:
        print("Value is not a number.")
    except SpotifyException as err:
        print("Error in volume:", err)


def next_song(sp_client, session=None):
    try:
        current_song = sp_client.currently_playing()
        if session is None:
            # print("next song has been pressed")
            # use spotify_rec to generate a recommendation, currently based on what song is playing for the user
            if current_song is not None:
                features = get_features(sp_client, current_song["item"]["name"])
                recommendation = spotify_rec_features(sp_client, current_song["item"]["name"], features)
            else:
                features = get_features(sp_client, "Red Rock Riviera")
                recommendation = spotify_rec_features(sp_client, "Red Rock Riviera", features)
            uri = recommendation
            # print(recommendation["tracks"][0]["name"])
            # add the generated recommendation to the queue
            queue_song(sp_client, uri)
            # go to the next song in queue
            sp_client.next_track()
        else:
            # print("next song has been pressed")
            # use spotify_rec to generate a recommendation, currently based on what song is playing for the user
            if current_song is not None:
                features = get_features(sp_client, current_song["item"]["name"])
                recommendation = spotify_rec_features(sp_client, current_song["item"]["name"], features,
                                                      session.get_likes(), session.get_dislikes())
            else:
                features = get_features(sp_client, "Red Rock Riviera")
                features["energy"] = features["energy"] + 0.01
                recommendation = spotify_rec_features(sp_client, "Red Rock Riviera", features)
            uri = recommendation
            # print(recommendation["tracks"][0]["name"])
            # add the generated recommendation to the queue
            if session.get_uri() == "" or session.get_uri() == current_song["item"]["uri"]:
                queue_song(sp_client, uri)
                session.set_uri(uri)
            elif session.get_uri() != current_song["item"]["uri"]:
                queue_song(sp_client, session.get_uri())
            # go to the next song in queue
            sp_client.next_track()
    except SpotifyException as err:
        print("Error in next song:", err)
    # need to go to next track in queue & use the recommendation algorithm
    # the problem may be that getting a recommendation is slower than pressing skip
    # for now the idea is to make pressing the button something that runs a recommendation call,
    # then adds it to queue
    # then goes to the next song in queue


def get_features(sp_client, track):
    results = sp_client.search(q="track:" + track, type="track")
    track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
    features = sp_client.audio_features(track_uri)[0]
    ret = {"danceability": features["danceability"], "energy": features["energy"], "valence": features["valence"]}
    return ret


# modified version of Kevin's method, returns info
# delete when recommendation is available
def serenity_spotify_rec(sp_client, track):
    # auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    # sp = spotipy.Spotify(auth_manager=auth)
    # membership = sp.current_user()["product"]
    # if membership != "premium":
    #    print("You are not authorized to access this")
    # else:
    results = sp_client.search(q="track:" + track, type="track")
    # print(results)
    artist_uri = [(results["tracks"]["items"][0]["artists"][0]["uri"]).split(":", 3)[2]]
    track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
    artistinfo = sp_client.artist(artist_uri[0])
    genres = artistinfo["genres"]
    rec = sp_client.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, seed_genres=[genres[0]], limit=1)
    return rec
    # image = rec["tracks"][0]["album"]["images"][0]["url"]
    # artist_name = (rec["tracks"][0]["artists"][0]["name"])
    # track_name = (rec["tracks"][0]["name"])
    # return image, artist_name, track_name


def spotify_rec_features(sp_client, track, features, likes=0, dislikes=0):
    print("Recommedation running")
    results = sp_client.search(q="track:" + track, type="track")
    artist_uri = [(results["tracks"]["items"][0]["artists"][0]["uri"]).split(":", 3)[2]]
    track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]

    rec = sp_client.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, limit=10,
                                    target_danceability=features["danceability"], target_energy=features["energy"],
                                    target_valence=features["valence"])
    current_song_uri = sp_client.currently_playing()["item"]["uri"]
    for each in rec["tracks"]:
        if each["uri"] != current_song_uri:
            return each["uri"]
    return spotify_rec_features(sp_client, track, features)


def get_devices(sp_client):
    devices = sp_client.devices()
    if len(devices['devices']) == 0:
        print("No available devices. Get a message through the app that they need a device to choose.")
        return None
    else:
        print("Devices SpotiVibe has detected it can use to play music from: ")
        device_number = 1
        for device in devices['devices']:
            print(f"Device {device_number}: {device['name']}")
            device_number += 1
        return devices


def set_device_id(dev_id):
    global di
    di = dev_id
    sp.transfer_playback(device_id=dev_id)


def get_device_id():
    return di


def get_device_volume():
    global dv, di
    devices = sp.devices()
    if di == "unselected" and len(devices['devices']) != 0:
        dv = int(devices['devices'][0]['volume_percent'])
    else:
        for device in devices['devices']:
            if device['id'] == di:
                dv = int(device['volume_percent'])
    return dv


def balance_values(features, likes, dislikes):
    new_features = {"danceability": features["danceability"], "energy": features["energy"],
                    "valence": features["valence"]}
    if likes > dislikes:  # if likes is greater than dislikes do not adjust anything
        return new_features
    elif likes == dislikes:  # Same amount of likes and dislikes slightly change all values
        adjust_values = 0.1
        if random() > 0.5:
            adjust_values = -adjust_values
    else:  # Dislikes is larger than likes more dramatic shift
        adjust_values = 0.3
        if random() > 0.5:
            adjust_values = -adjust_values
    new_features["danceability"] = max(1, min(0, round(features["danceability"] + adjust_values, 3)))
    new_features["energy"] = max(1, min(0, round(features["energy"] + adjust_values, 3)))
    new_features["valence"] = max(1, min(0, round(features["valence"] + adjust_values, 3)))
    return new_features


# note: redirect URI needs to have a port and be http, not https
auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=auth)
# plan to initialize a session history when a new listening session is created
session_history = list()

membership = sp.current_user()["product"]