import time
from datetime import datetime

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyPKCE

from src.database.session import Session, get_session

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


def queue_song(sp, uri, session=None):
    try:
        sp.add_to_queue(uri)
        # this is going to be interesting - the session history is shared across users, sp is local to each user.
        # maybe solution should be to give this a list of each user's sp's to add to each queue individually?
        if session is not None:
            print("queue_song: session is *not* none")
            print(session)
            track = sp.track(uri)
            session.update_session_history(uri, name=track["name"])
        else:
            print("queue_song: session is none")
            print(session)
            session_history.append(uri)
    except SpotifyException as err:
        print("Error in enqueue:", err)


def make_playlist_from_history(sp):
    user_id = sp.current_user()["id"]
    dtstring = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    playlist = sp.user_playlist_create(user=user_id, name=dtstring, description="Created by Spotivibe.")["id"]
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist, tracks=session_history)


def play_button_functionality(sp, di, session=None):
    try:
        currently_playing = sp.currently_playing()
        print(currently_playing)
        if session is not None and session.get_uri() != "" and session.get_uri() != currently_playing["item"]["uri"]:
            queue_song(sp, session.get_uri(), session=session)
            sp.next_track()
        if currently_playing is None:
            print("No track playing. Greyed out play button.")
        elif currently_playing["is_playing"] is False:
            sp.start_playback(device_id=di)
        elif currently_playing["is_playing"] is True:
            sp.pause_playback(device_id=di)
    except SpotifyException as err:
        print("Error in play button:", err)


def volume_functionality(sp, volume):
    vol = int(volume)
    try:
        if 0 <= vol <= 100:
            # do this for now,
            sp.volume(vol)
        else:
            print("Invalid volume percentage number. Ignore volume set")
    except ValueError:
        print("Value is not a number.")
    except SpotifyException as err:
        print("Error in volume:", err)


def next_song(sp, session=None):
    try:
        if session == None:
            print("next song has been pressed")
            # use spotify_rec to generate a recommendation, currently based on what song is playing for the user
            currently_playing = sp.currently_playing()
            if currently_playing is not None:
                features = get_features(sp, currently_playing["item"]["name"])
                recommendation = spotify_rec_features(sp, currently_playing["item"]["name"], features)
            else:
                features = get_features(sp, "Red Rock Riviera")
                recommendation = spotify_rec_features(sp, "Red Rock Riviera", features)
            uri = recommendation["tracks"][0]["uri"]
            print(recommendation["tracks"][0]["name"])
            # add the generated recommendation to the queue
            queue_song(sp, uri)
            # go to the next song in queue
            sp.next_track()
        else:
            print("next song has been pressed")
            # use spotify_rec to generate a recommendation, currently based on what song is playing for the user
            currently_playing = sp.currently_playing()
            if currently_playing is not None:
                features = get_features(sp, currently_playing["item"]["name"])
                recommendation = spotify_rec_features(sp, currently_playing["item"]["name"], features)
            else:
                features = get_features(sp, "Red Rock Riviera")
                features["energy"] = features["energy"] + 0.01
                recommendation = spotify_rec_features(sp, "Red Rock Riviera", features)
            uri = recommendation["tracks"][0]["uri"]
            # print(recommendation["tracks"][0]["name"])
            # add the generated recommendation to the queue
            if session.get_uri() == "" or session.get_uri() == sp.currently_playing()["item"]["uri"]:
                queue_song(sp, uri, session=session)
                session.set_uri(uri)
            elif session.get_uri() != sp.currently_playing()["item"]["uri"]:
                queue_song(sp, session.get_uri(), session=session)
            # go to the next song in queue
            sp.next_track()
    except SpotifyException as err:
        print("Error in next song:", err)
    # need to go to next track in queue & use the recommendation algorithm
    # the problem may be that getting a recommendation is slower than pressing skip
    # for now the idea is to make pressing the button something that runs a recommendation call,
    # then adds it to queue
    # then goes to the next song in queue


def get_features(sp, track):
    results = sp.search(q="track:" + track, type="track")
    track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
    features = sp.audio_features(track_uri)[0]
    ret = {"danceability": features["danceability"], "energy": features["energy"], "valence": features["valence"]}
    return ret


# modified version of Kevin's method, returns info
# delete when recommendation is available
def serenity_spotify_rec(sp, track):
    # auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    # sp = spotipy.Spotify(auth_manager=auth)
    # membership = sp.current_user()["product"]
    # if membership != "premium":
    #    print("You are not authorized to access this")
    # else:
    results = sp.search(q="track:" + track, type="track")
    # print(results)
    artist_uri = [(results["tracks"]["items"][0]["artists"][0]["uri"]).split(":", 3)[2]]
    track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
    artistinfo = sp.artist(artist_uri[0])
    genres = artistinfo["genres"]
    rec = sp.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, seed_genres=[genres[0]], limit=1)
    return rec
    # image = rec["tracks"][0]["album"]["images"][0]["url"]
    # artist_name = (rec["tracks"][0]["artists"][0]["name"])
    # track_name = (rec["tracks"][0]["name"])
    # return image, artist_name, track_name


def spotify_rec_features(sp, track, features):
    print("Recommedation running")
    results = sp.search(q="track:" + track, type="track")
    artist_uri = [(results["tracks"]["items"][0]["artists"][0]["uri"]).split(":", 3)[2]]
    track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
    # artistinfo = sp.artist(artist_uri[0])
    # if artistinfo["genres"]:
    #    rec = sp.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, seed_genres=[artistinfo["genres"][0]],
    #                             limit=10, target_danceability=features["danceability"],
    #                             target_energy=features["energy"], target_valence=features["valence"])
    # else:
    rec = sp.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, limit=10,
                             target_danceability=features["danceability"], target_energy=features["energy"],
                             target_valence=features["valence"])
    if rec["tracks"][0]["uri"] == sp.currently_playing()["item"]["uri"]:
        return spotify_rec_features(sp, track, features)
    return rec


def get_devices(sp):
    devices = sp.devices()
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


# note: redirect URI needs to have a port and be http, not https
auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=auth)
# plan to initialize a session history when a new listening session is created
session_history = list()

membership = sp.current_user()["product"]

# print(spotify_rec_features(sp, "Little Lion Man", []))
# keepLooping = 1
# choice = 0

'''
# code will be going into tab2.ky or py?
if membership != "premium":
    print("You are not authorized to access this")
else:
    di = choose_device(sp)
    current = sp.currently_playing()
    print(current)
    current_uri = current["item"]["uri"]
    session_history.append(current_uri)
    while keepLooping:
        print("Options! Press 1 to use the play/pause button")
        print("Press 2 to enter a volume percentage")
        print("Press 3 to skip current song to a new recommendation.")
        print("Press 4 to change playback device.")
        print("Press 5 to show the session history.")
        print("Press 6 to create a playlist from session history.")
        choice = input('Press any other key to exit.')
        if choice == "1":
            play_button_functionality(sp, di)
        elif choice == "2":
            vol = input('Enter a number between 0 and 100 to set the player volume.')
            volume_functionality(sp, vol)
        elif choice == "3":
            next_song(sp)
        elif choice == "4":
            di = choose_device(sp)
        elif choice == "5":
            print("Showing session history (list of URIs)...")
            print(session_history)
            for e in session_history:
                print(get_data_from_track_uri(e))
        elif choice == "6":
            print("Making playlist...")
            make_playlist_from_history(sp)
            print("Done! Check your Spotify.")
        else:
            exit(0)
'''
