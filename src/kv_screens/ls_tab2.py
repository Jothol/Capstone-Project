import threading
import time

import kivy
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens import player

kivy.require('2.3.0')

sp = player.sp
di = "unselected"





class LS_Tab2(Screen):
    index = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        sm.ids.check = None
        self.add_widget(sm)

    def on_enter(self, *args):
        self.ids.session_name = self.manager.parent.parent.parent.ids.session_name
        self.ids.check = Clock.schedule_interval(self.get_current_song, 5)

    def get_current_song(self, dt):
        # print("Testing")
        current = sp.currently_playing()
        if self.ids.session_name.get_uri() == "" and current is not None:
            self.ids.session_name.set_uri(current["item"]["uri"])
        elif self.ids.session_name.get_uri() != "" and self.ids.session_name.get_uri() != \
                current["item"]["uri"]:
            player.queue_song(sp, self.ids.session_name.get_uri())
            sp.next_track()

    def on_leave(self, *args):
        Clock.unschedule(self.get_current_song)

    def restart(self):
        pass

    def play(self):
        global di
        currently_playing = sp.currently_playing()
        if di != "unselected":
            player.play_button_functionality(sp=sp, di=di, session=self.ids.session_name)
            if currently_playing["is_playing"] is False:
                self.ids.play_icon.source = '../other/images/pause_icon.png'
            else:
                self.ids.play_icon.source = '../other/images/play_icon.png'
        else:
            if currently_playing is not None:
                self.ids.play_icon.source = '../other/images/pause_icon.png'
                di = sp.devices()['devices'][0]['id']
                player.play_button_functionality(sp, di, self.ids.session_name)

    def skip(self):
        player.next_song(sp, session=self.ids.session_name)

    def volume(self, value):
        print(value)
        player.volume_functionality(sp, value)

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


