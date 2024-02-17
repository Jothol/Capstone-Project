import os
import kivy
import spotipy
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from spotipy.oauth2 import SpotifyOAuth, SpotifyPKCE
from kivy.app import App

kivy.require('2.3.0')

scope = ("user-read-playback-state user-modify-playback-state user-read-currently-playing streaming "
         "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public "
         "user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played "
         "user-library-modify user-library-read user-read-email user-read-private")
SPOTIPY_CLIENT_ID = '66880bb5822a48459696468e620a10d6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080'


def spotify_rec(track):
    auth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth)
    membership = sp.current_user()["product"]
    if membership != "premium":
        print("You are not authorized to access this")
    else:
        results = sp.search(q="track:"+track, type="track")

        artist_uri = [(results["tracks"]["items"][0]["artists"][0]["uri"]).split(":", 3)[2]]
        track_uri = [(results["tracks"]["items"][0]["uri"]).split(":", 3)[2]]
        artistinfo = sp.artist(artist_uri[0])
        genres = artistinfo["genres"]
        rec = sp.recommendations(seed_artists=artist_uri, seed_tracks=track_uri, seed_genres=[genres[0]], limit=1)
        image = rec["tracks"][0]["album"]["images"][0]["url"]
        artist_name = (rec["tracks"][0]["artists"][0]["name"])
        track_name = (rec["tracks"][0]["name"])
        return image, artist_name, track_name


class RecommendationsTest(Widget):
    image_source = StringProperty()
    Artist_text = StringProperty("Artist Name")
    Song_text = StringProperty("Song Title")


class RecommendationApp(App):

    def build(self):
        cwd = os.getcwd()
        self.root = Builder.load_file(cwd + '/kv_style/RecommendationsTest.kv')
        track = input("Enter a Song Name")
        image, artist_name, track_name = spotify_rec(track)
        app = RecommendationsTest()
        app.image_source = image
        app.Artist_text = artist_name
        app.Song_text = track_name
        return app

    def rerun_app(self):
        self.stop()  # Stop the current app instance
        RecommendationApp().run()


if __name__ == "__main__":
    spotify_rec("Let It Be")
