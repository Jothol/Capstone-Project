import kivy
from kivy.animation import Animation
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')


class Tab2(Screen):
    index = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Tab 2!"))

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
        control_buttons = self.ids.control_buttons

        if player_window.y < -250:
            animation_controls = Animation(pos=(control_buttons.x, control_buttons.y + dp(50)), duration=0.1)
            animation_window = Animation(pos=(player_window.x, player_window.y + dp(400)), duration=0.1)

        else:
            animation_window = Animation(pos=(player_window.x, player_window.y - dp(400)), duration=0.1)
            animation_controls = Animation(pos=(control_buttons.x, control_buttons.y - dp(50)), duration=0.1)

        animation_window.start(player_window)
        animation_controls.start(control_buttons)