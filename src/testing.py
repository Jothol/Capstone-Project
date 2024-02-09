import os

import spotipy
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from spotipy.oauth2 import SpotifyOAuth
import kivy

kivy.require('2.3.0')  # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label

scope = ("user-read-playback-state user-modify-playback-state user-read-currently-playing streaming "
         "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public "
         "user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played "
         "user-library-modify user-library-read user-read-email user-read-private")


def spotify_rec():
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
        image, artist_name, track_name = spotify_rec()
        app = RecommendationsTest()
        app.image_source = image
        app.Artist_text = artist_name
        app.Song_text = track_name
        return app

    def rerun_app(self):
        self.stop()  # Stop the current app instance
        RecommendationApp().run()

if __name__ == "__main__":
    cwd = os.getcwd()
    Builder.load_file(cwd + '/kv_style/RecommendationsTest.kv')
    RecommendationApp().run()
