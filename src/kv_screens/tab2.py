import kivy
from spotipy import SpotifyException
from kivy.animation import Animation
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens import player, volume_slider

kivy.require('2.3.0')

sp = player.sp


def volume(slider):
    player.volume_functionality(sp, slider.value)


class Tab2(Screen):
    index = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Tab 2!"))
        starting_volume = player.get_device_volume()
        volume_slider_instance = volume_slider.VolumeSlider(value=starting_volume)
        volume_slider_instance.bind(on_release=volume)
        volume_slider_instance.bind(value=self.update_slider_label)
        volume_percentage_label = Label(text=f"Volume: {starting_volume}%", color=[0, 0, 0, 1])
        volume_percentage_label.id = 'volume_label'
        self.ids.volume_box.add_widget(volume_slider_instance)
        self.ids.volume_box.add_widget(volume_percentage_label)
        self.update_play_button()

    def on_enter(self, *args):
        self.update_play_button()

    def restart(self):
        pass

    def play(self):
        di = player.get_device_id()
        currently_playing = sp.currently_playing()
        if di != "unselected":
            player.play_button_functionality(sp=sp, di=di)
            self.update_play_button()
        else:
            if currently_playing is not None:
                di = sp.devices()['devices'][0]['id']
                player.play_button_functionality(sp, di)
                self.update_play_button()

    def skip(self):
        player.next_song(sp)

    def update_slider_label(self, slider, value):
        self.ids.volume_box.children[0].text = f"Volume: {int(value)}%"

    def update_play_button(self, current=None):
        if current is None:
            current = sp.currently_playing()
            if current is None:
                self.ids.play_icon.source = '../other/images/play_icon.png'
        if current["is_playing"] is True:
            self.ids.play_icon.source = '../other/images/pause_icon.png'
        else:
            self.ids.play_icon.source = '../other/images/play_icon.png'

    def spotify_search(self):
        search_text = self.ids.search_input.text
        try:
            results = sp.search(q=search_text, type="track", limit=5)
            print("Results of search", results)
            i = 0
            for track in results["tracks"]["items"]:
                i += 1
                print("Track " + str(i) + ":", track["name"] + ", by", track["artists"][0]["name"])
        except SpotifyException as err:
            print("Error in spotify_search:", err)

    def shuffle(self):
        pass

    def like(self):
        pass

    def dislike(self):
        pass

    def animate_player(self):
        player_window = self.ids.player_window
        control_buttons = self.ids.control_buttons

        if player_window.y < -250:
            animation_controls = Animation(pos=(control_buttons.x, control_buttons.y + dp(50)), duration=0.1)
            animation_window = Animation(pos=(player_window.x, player_window.y + dp(400)), duration=0.1)

        else:
            animation_window = Animation(pos=(player_window.x, player_window.y - dp(400)), duration=0.1)
            animation_controls = Animation(pos=(control_buttons.x, control_buttons.y - dp(50)), duration=0.1)

        animation_window.start(player_window)
        animation_controls.start(control_buttons)