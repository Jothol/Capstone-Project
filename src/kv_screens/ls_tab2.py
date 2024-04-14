import time

import kivy
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens import player, volume_slider

kivy.require('2.3.0')

sp = player.sp
di = "unselected"


def volume(slider):
    player.volume_functionality(sp, slider.value)


class LS_Tab2(Screen):
    index = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        sm.ids.check = None
        sm.ids.like_pushed = False
        sm.ids.dislike_pushed = False
        sm.ids.song_length = None
        self.add_widget(sm)
        starting_volume = player.get_device_volume()
        volume_slider_instance = volume_slider.VolumeSlider(value=starting_volume)
        volume_slider_instance.bind(on_release=volume)
        volume_slider_instance.bind(value=self.update_slider_label)
        volume_percentage_label = Label(text=f"Volume: {starting_volume}%", color=[0, 0, 0, 1])
        volume_percentage_label.id = 'volume_label'
        self.ids.volume_box.add_widget(volume_slider_instance)
        self.ids.volume_box.add_widget(volume_percentage_label)

    def on_enter(self, *args):
        self.ids.like_pushed = False
        self.ids.dislike_pushed = False
        self.ids.song_length = None
        self.ids.session_name = self.manager.parent.parent.parent.ids.session_name
        self.ids.check = Clock.schedule_interval(self.get_current_song, 5)

    def get_current_song(self, dt):
        # print("Testing")
        current = sp.currently_playing()
        try:
            if self.ids.session_name.get_uri() == "" and current is not None:
                self.ids.session_name.set_uri(current["item"]["uri"])
            elif self.ids.session_name.get_uri() != "" and self.ids.session_name.get_uri() != \
                    current["item"]["uri"]:
                player.queue_song(sp, self.ids.session_name.get_uri())
                sp.next_track()
        except Exception as e:
            self.on_leave()

    def on_leave(self, *args):
        Clock.unschedule(self.ids.check)
        if self.ids.song_length is not None:
            self.ids.song_length.cancel()

    def restart(self):
        pass

    def play(self):
        global di
        currently_playing = sp.currently_playing()
        if di != "unselected":
            player.play_button_functionality(sp_client=sp, listening_device=di, session=self.ids.session_name)
            if currently_playing["is_playing"] is False:
                self.ids.play_icon.source = '../other/images/pause_icon.png'
            else:
                self.ids.play_icon.source = '../other/images/play_icon.png'
        else:
            if currently_playing is not None:
                self.ids.play_icon.source = '../other/images/pause_icon.png'
                di = sp.devices()['devices'][0]['id']
                player.play_button_functionality(sp, di, self.ids.session_name)

    def skip(self, td=None):
        # print(self.ids.session_name)
        if self.ids.song_length is not None:
            self.ids.song_length.cancel()
        player.next_song(sp, session=self.ids.session_name)
        self.ids.session_name.reset_likes_and_dislikes()
        self.ids.like_pushed = False
        self.ids.dislike_pushed = False
        time.sleep(1)  # Sleeps to ensure that the current song is the new song
        milli_sec = float(sp.currently_playing()["item"]["duration_ms"])
        song_length = (milli_sec / 1000.0)
        print(f"Song length => {int(song_length / 60)}:{int(song_length % 60)}")
        self.ids.song_length = Clock.schedule_once(self.skip, 30)

    def update_slider_label(self, slider, value):
        self.ids.volume_box.children[0].text = f"Volume: {int(value)}%"

    def shuffle(self):
        pass

    def like(self):
        if self.ids.dislike_pushed:
            self.ids.session_name.increment_likes()
            self.ids.session_name.decrement_dislikes()
            self.ids.dislike_pushed = False
            self.ids.like_pushed = True
        elif not self.ids.like_pushed:
            self.ids.session_name.increment_likes()
            self.ids.like_pushed = True
            self.ids.dislike_pushed = False

    def dislike(self):
        if self.ids.like_pushed:
            self.ids.session_name.decrement_likes()
            self.ids.session_name.increment_dislikes()
            self.ids.like_pushed = False
            self.ids.dislike_pushed = True
        elif not self.ids.dislike_pushed:
            self.ids.session_name.increment_dislikes()
            self.ids.dislike_pushed = True
            self.ids.like_pushed = False

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
