import kivy
from kivy.animation import Animation
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens import player

kivy.require('2.3.0')

sp = player.sp


class VolumeSlider(Slider):
    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        self.step = 1
        self.min = 0
        self.max = 100
        self.id = "volume_slider"
        # self.value = TODO: initialize with users current device volume
        super(VolumeSlider, self).__init__(**kwargs)

    def on_release(self):
        pass

    def on_touch_up(self, touch):
        super(VolumeSlider, self).on_touch_up(touch)
        if touch.grab_current == self:
            self.dispatch('on_release')
            return True


def volume(slider):
    print(slider.value)
    player.volume_functionality(sp, slider.value)


class Tab2(Screen):
    index = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Tab 2!"))
        volume_slider_instance = VolumeSlider()
        volume_slider_instance.bind(on_release=volume)
        volume_slider_instance.bind(value=self.update_slider_label)
        self.ids.volume_slider_placeholder.add_widget(volume_slider_instance)

    def on_enter(self, *args):
        pass

    def restart(self):
        pass

    def play(self):
        di = player.get_device_id()
        currently_playing = sp.currently_playing()
        if di != "unselected":
            player.play_button_functionality(sp=sp, di=di)
            if currently_playing is None:
                print("Nothing is playing or queued to play. Do nothing for play button.")
            elif currently_playing["is_playing"] is False:
                self.ids.play_icon.source = '../other/images/pause_icon.png'
            else:
                self.ids.play_icon.source = '../other/images/play_icon.png'
        else:
            if currently_playing is not None:
                self.ids.play_icon.source = '../other/images/pause_icon.png'
                di = sp.devices()['devices'][0]['id']
                player.play_button_functionality(sp, di)

    def skip(self):
        player.next_song(sp)

    def update_slider_label(self, slider, value):
        print(slider)
        print(value)
        self.ids.volume_label.text = f"Volume: {int(value)}%"

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