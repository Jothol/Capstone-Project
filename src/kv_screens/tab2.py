import kivy
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')


class Tab2(Screen):
    index = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def restart(self):
        pass

    def play(self):
        if self.ids.play_icon.source == '../other/images/play_icon.png':
            self.ids.play_icon.source = '../other/images/pause_icon.png'
        else:
            self.ids.play_icon.source = '../other/images/play_icon.png'

    def skip(self):
        pass

    def shuffle(self):
        pass

    def like(self):
        pass

    def dislike(self):
        pass

    def animate_player(self):
        player_window = self.ids.player_window
        if player_window.y < -250:
            animation = Animation(pos=(player_window.x, player_window.y + dp(400)), duration=0.2)
        else:
            animation = Animation(pos=(player_window.x, player_window.y - dp(400)), duration=0.2)
        animation.start(player_window)
