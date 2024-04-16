import threading
import time

import kivy
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens import player, volume_slider
from src.kv_screens import ls_tab3

kivy.require('2.3.0')

sp = player.sp
di = "unselected"


def volume(slider):
    player.volume_functionality(sp, slider.value)


class LS_Tab2(Screen):
    index = 2
    song_list = ""
    likes = 0
    dislikes = 0
    likes_pressed = False
    dislikes_pressed = False
    already_added = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        sm.ids.check = None
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
        self.ids.session_name = self.manager.parent.parent.parent.ids.session_name
        self.ids.check = Clock.schedule_interval(self.get_current_song, 5)

    def get_current_song(self, dt):
        # print("Testing")
        if self.ids.session_name.name is None:
            return

        current = sp.currently_playing()
        if self.ids.session_name.get_uri() == "" and current is not None:
            self.ids.session_name.set_uri(current["item"]["uri"])
            # Below is added part for song history to save
            self.ids.session_name.set_album(current["item"]["album"]["name"])
            self.ids.session_name.set_artists(current["item"]["artists"])
            self.ids.session_name.set_current_song(current["item"]["name"])
            song_name = current["item"]["name"]
            artist_names = self.ids.session_name.get_artists()
            song_entry = song_name + ": " + artist_names

            index = LS_Tab2.song_list.find(song_entry)
            if index == -1:  # checks if song name is not already included
                # adding new played song into list
                if LS_Tab2.song_list == "":
                    LS_Tab2.song_list = song_entry
                else:
                    LS_Tab2.song_list += "     " + song_entry
                self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
        elif self.ids.session_name.get_uri() != "" and self.ids.session_name.get_uri() != \
                current["item"]["uri"]:
            player.queue_song(sp, self.ids.session_name.get_uri())
            sp.next_track()
            # Below is added part for song history to save
            current = sp.currently_playing()
            song_name = current["item"]["name"]
            artist_names = self.ids.session_name.get_artists()
            song_entry = song_name + ": " + artist_names
            index = LS_Tab2.song_list.find(song_entry)
            if index == -1:  # checks if song name is not already included
                if LS_Tab2.song_list == "":
                    LS_Tab2.song_list = song_entry
                else:
                    LS_Tab2.song_list += "     " + song_entry
                # self.ids.song_info.text = LS_Tab2.song_list
                self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
        elif self.ids.session_name.get_uri() == current["item"]["uri"]:
            # purpose is to check the amount of likes and dislikes and if color text needs to be updated
            LS_Tab2.likes = self.ids.session_name.get_likes()
            LS_Tab2.dislikes = self.ids.session_name.get_dislikes()
            song_entry = self.ids.session_name.get_current_song() + ": " + self.ids.session_name.get_artists()
            index = LS_Tab2.song_list.find(song_entry)  # locates first letter for song_entry
            if LS_Tab2.song_list[index-7:index-1] == "00ff00":  # currently green text favoring likes
                if LS_Tab2.likes < LS_Tab2.dislikes:  # text changes from green to red
                    print("change from green to red")
                    LS_Tab2.song_list = LS_Tab2.song_list[:index-7]+"ff0000"+LS_Tab2.song_list[index-1:]
                    self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
                elif LS_Tab2.likes == LS_Tab2.dislikes:  # change text color back to normal
                    print("change back to normal color")
                    LS_Tab2.song_list = LS_Tab2.song_list[:index - 14] + LS_Tab2.song_list[index:len(LS_Tab2.song_list)-8]
                    self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
            elif LS_Tab2.song_list[index-7:index-1] == "ff0000":  # current red text favoring dislikes
                if LS_Tab2.likes > LS_Tab2.dislikes:  # text changes from red to green
                    print("change from red to green")
                    LS_Tab2.song_list = LS_Tab2.song_list[:index - 7] + "00ff00" + LS_Tab2.song_list[index - 1:]
                    self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
                elif LS_Tab2.likes == LS_Tab2.dislikes:  # change text color back to normal
                    print("change back to normal color", LS_Tab2.song_list[:index-14])
                    # print(LS_Tab2.song_list[index:len(LS_Tab2.song_list)-8])
                    LS_Tab2.song_list = LS_Tab2.song_list[:index - 14]+LS_Tab2.song_list[index:len(LS_Tab2.song_list)-8]

                    self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
            else:  # text color is normal favoring neither likes or dislikes
                if LS_Tab2.likes < LS_Tab2.dislikes:  # change text from normal to red
                    print("NO IN HERE")
                    print("boy", LS_Tab2.song_list[:index])
                    LS_Tab2.song_list = LS_Tab2.song_list[:index] + "[color=ff0000]" + song_entry + "[/color]"
                    print("after", LS_Tab2.song_list)
                    self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})
                elif LS_Tab2.likes > LS_Tab2.dislikes:  # change text from normal to green
                    print("IT IS IN HERE")
                    LS_Tab2.song_list = LS_Tab2.song_list[:index] + "[color=00ff00]" + song_entry + "[/color]"
                    self.ids.session_name.saved_song.update({'songs_played': LS_Tab2.song_list})


    def on_leave(self, *args):
        Clock.unschedule(self.ids.check)

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
        LS_Tab2.likes_pressed = False
        LS_Tab2.dislikes_pressed = False

    def update_slider_label(self, slider, value):
        self.ids.volume_box.children[0].text = f"Volume: {int(value)}%"

    def shuffle(self):
        pass

    def like(self):
        if LS_Tab2.likes_pressed is False:
            self.ids.session_name.increment_likes()
            LS_Tab2.likes_pressed = True
            if LS_Tab2.dislikes_pressed is True:
                self.ids.session_name.decrement_dislikes()
                LS_Tab2.dislikes_pressed = False
        else:
            self.ids.session_name.decrement_likes()
            LS_Tab2.likes_pressed = False

    def dislike(self):
        if LS_Tab2.dislikes_pressed is False:
            self.ids.session_name.increment_dislikes()
            LS_Tab2.dislikes_pressed = True
            if LS_Tab2.likes_pressed is True:
                self.ids.session_name.decrement_likes()
                LS_Tab2.likes_pressed = False
        else:
            self.ids.session_name.decrement_dislikes()
            LS_Tab2.dislikes_pressed = False

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
