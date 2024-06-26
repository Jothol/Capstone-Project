import time

import kivy
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens import player
from src.database import volume_slider

kivy.require('2.3.0')

sp = player.sp
di = "unselected"
check = None


def volume(slider):
    player.volume_functionality(sp, slider.value)


class LsTab2(Screen):
    global check
    index = 2
    song_list = ""
    current_song = ""
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
        sm.ids.like_pushed = False
        sm.ids.dislike_pushed = False
        self.song_length = None
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
        global check
        self.ids.session_name = self.manager.parent.parent.parent.ids.session_name
        current = sp.currently_playing()
        if current is not None:
            if current["item"]["uri"] != self.ids.session_name.get_uri():
                LsTab2.likes_pressed = False
                LsTab2.dislikes_pressed = False

        self.ids.like_pushed = LsTab2.likes_pressed
        self.ids.dislike_pushed = LsTab2.dislikes_pressed
        self.song_length = None
        check = Clock.schedule_interval(self.get_current_song, 10)
        self.update_play_button()
        LsTab2.song_list = self.ids.session_name.saved_song.get().get("songs_played")
        LsTab2.current_song = self.ids.session_name.get_current_song() + ": " + self.ids.session_name.get_artists()

    def get_current_song(self, dt):
        # print("Testing")
        current = sp.currently_playing()
        # self.update_play_button(current=current)
        try:
            if self.ids.session_name.get_uri() == "" and current is not None:
                self.ids.session_name.set_uri(current["item"]["uri"])
                # Below is added part for song history to save
                self.ids.session_name.set_album(current["item"]["album"]["name"])
                self.ids.session_name.set_artists(current["item"]["artists"])
                self.ids.session_name.set_current_song(current["item"]["name"])
                song_name = current["item"]["name"]
                artist_names = self.ids.session_name.get_artists()
                song_entry = song_name + ": " + artist_names
                LsTab2.current_song = song_entry

                index = LsTab2.song_list.find(song_entry)
                if index == -1:  # checks if song name is not already included
                    # adding new played song into list
                    if LsTab2.song_list == "":
                        LsTab2.song_list = song_entry
                    else:
                        LsTab2.song_list += "     " + song_entry
                    self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
            elif self.ids.session_name.get_uri() != "" and self.ids.session_name.get_uri() != \
                    current["item"]["uri"]:
                player.queue_song(sp, self.ids.session_name.get_uri())
                sp.next_track()
            elif self.ids.session_name.get_uri() == current["item"]["uri"]:
                # purpose is to check the amount of likes and dislikes and if color text needs to be updated
                LsTab2.likes = self.ids.session_name.get_likes()
                LsTab2.dislikes = self.ids.session_name.get_dislikes()
                song_entry = self.ids.session_name.get_current_song() + ": " + self.ids.session_name.get_artists()
                LsTab2.current_song = song_entry
                index = LsTab2.song_list.find(song_entry)  # locates first letter for song_entry
                if index == -1:  # check if song_entry has been entered in the session settings songs played
                    # adding new played song into list
                    if LsTab2.song_list == "":
                        LsTab2.song_list = song_entry
                    else:
                        LsTab2.song_list += "     " + song_entry
                    self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
                    return

        except Exception as e:
            print(e)
            self.on_leave()

    def on_leave(self, *args):
        global check
        if check is not None:
            check.cancel()
        if self.song_length is not None:
            self.song_length.cancel()

    def restart(self):
        pass

    def play(self):
        global check
        global di
        if check is not None:
            check.cancel()
        if di != "unselected":
            player.play_button_functionality(sp, di, session=self.ids.session_name)
            self.update_play_button()
        else:
            if sp.currently_playing() is not None:
                self.update_play_button()
                di = sp.devices()['devices'][0]['id']
                player.play_button_functionality(sp, di, self.ids.session_name)

    def skip(self, dt=None):
        global check
        # print(self.ids.session_name)
        # print("Skip button")
        check.cancel()
        if self.song_length is not None:
            self.song_length.cancel()
        player.next_song(sp, session=self.ids.session_name)
        self.ids.session_name.reset_likes_and_dislikes()
        self.ids.like_pushed = False
        self.ids.dislike_pushed = False
        LsTab2.current_song = self.ids.session_name.get_current_song() + ": " + self.ids.session_name.get_artists()
        time.sleep(3)  # Sleeps to ensure that the current song is the new song
        milli_sec = float(sp.currently_playing()["item"]["duration_ms"])
        song_length = (milli_sec / 1000.0) - 2
        # print(f"Song length => {int(song_length / 60)}:{int(song_length % 60)}")
        self.song_length = Clock.schedule_once(self.skip, timeout=song_length)
        check()
        LsTab2.likes_pressed = False
        LsTab2.dislikes_pressed = False

    def update_slider_label(self, slider, value):
        self.ids.volume_box.children[0].text = f"Volume: {int(value)}%"

    def update_play_button(self, current=None):
        global check
        if current is None:
            current = sp.currently_playing()
            if current is None:
                self.ids.play_icon.source = '../other/images/play_icon.png'
                return
        if current["is_playing"] is True:
            if self.song_length is not None:
                self.song_length.cancel()
            length_s = float(current["item"]["duration_ms"]) / 1000.0
            progress_s = float(current["progress_ms"]) / 1000.0
            # print(f"{(length_s - progress_s - 2)} time left")
            self.song_length = Clock.schedule_once(self.skip, timeout=(length_s - progress_s - 2))
            check()
            self.ids.play_icon.source = '../other/images/pause_icon.png'
            self.ids.play_icon.source = '../other/images/pause_icon.png'
        else:
            if self.song_length is not None:
                self.song_length.cancel()
            self.ids.play_icon.source = '../other/images/play_icon.png'

    def like(self):
        # User already liked the song
        if self.ids.like_pushed:
            self.ids.session_name.decrement_likes()
            self.ids.like_pushed = False
            LsTab2.likes_pressed = False
            LsTab2.likes = self.ids.session_name.get_likes()
            LsTab2.dislikes = self.ids.session_name.get_dislikes()

            # Checking the different situations of unpressing the like button
            index = LsTab2.song_list.find(LsTab2.current_song)
            # Unpressing the like button does not affect anything since there were already more dislikes
            if LsTab2.song_list[index - 7:index - 1] == "ff0000":
                return
            # Unpressing the like caused 1 more dislikes than likes
            elif LsTab2.likes < LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index] + "[color=ff0000]" + LsTab2.current_song + "[/color]"
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
            elif LsTab2.likes == LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index - 14] + LsTab2.song_list[index:len(LsTab2.song_list) - 8]
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})

            return

        # Rest are situations where the user did not press the like button

        # Checks the dislike button was already pushed
        if self.ids.dislike_pushed:
            self.ids.session_name.increment_likes()
            self.ids.session_name.decrement_dislikes()
            self.ids.dislike_pushed = False
            self.ids.like_pushed = True
            LsTab2.likes_pressed = True
            LsTab2.dislikes_pressed = False
        # Checks that the like button was not pushed
        elif not self.ids.like_pushed:
            self.ids.session_name.increment_likes()
            self.ids.like_pushed = True
            self.ids.dislike_pushed = False
            LsTab2.likes_pressed = True
            LsTab2.dislikes_pressed = False

        LsTab2.likes = self.ids.session_name.get_likes()
        LsTab2.dislikes = self.ids.session_name.get_dislikes()

        # Pressing like button caused more likes than dislikes
        index = LsTab2.song_list.find(LsTab2.current_song)
        # Was previously more dislikes than likes
        if LsTab2.song_list[index - 7:index - 1] == "ff0000":
            if LsTab2.likes == LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index - 14] + LsTab2.song_list[index:len(LsTab2.song_list) - 8]
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
            elif LsTab2.likes > LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index - 7] + "00ff00" + LsTab2.song_list[index - 1:]
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
        # Already had more likes than dislikes
        elif LsTab2.song_list[index - 7:index - 1] == "ff0000":
            return
        # Was even amount of likes and dislikes before pressed
        else:
            LsTab2.song_list = LsTab2.song_list[:index] + "[color=00ff00]" + LsTab2.current_song + "[/color]"
            self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})


    def dislike(self):
        if self.ids.dislike_pushed:
            self.ids.session_name.decrement_dislikes()
            self.ids.dislike_pushed = False
            LsTab2.dislikes_pressed = False
            LsTab2.likes = self.ids.session_name.get_likes()
            LsTab2.dislikes = self.ids.session_name.get_dislikes()

            # Checking the different situations of unpressing the like button
            index = LsTab2.song_list.find(LsTab2.current_song)
            # Unpressing the dislike button does not affect anything since there were already more likes
            if LsTab2.song_list[index - 7:index - 1] == "00ff00":
                return
            # Unpressing the dislike caused 1 more likes than dislikes
            elif LsTab2.likes > LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index] + "[color=00ff00]" + LsTab2.current_song + "[/color]"
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
            elif LsTab2.likes == LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index - 14] + LsTab2.song_list[index:len(LsTab2.song_list) - 8]
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})

            return

        # Rest are situations where the user did not press the like button

        # Checks the dislike button was already pushed
        if self.ids.like_pushed:
            self.ids.session_name.increment_dislikes()
            self.ids.session_name.decrement_likes()
            self.ids.like_pushed = False
            self.ids.dislike_pushed = True
            LsTab2.dislikes_pressed = True
            LsTab2.likes_pressed = False
        # Checks that the like button was not pushed
        elif not self.ids.dislike_pushed:
            self.ids.session_name.increment_dislikes()
            self.ids.dislike_pushed = True
            self.ids.like_pushed = False
            LsTab2.dislikes_pressed = True
            LsTab2.likes_pressed = False

        LsTab2.likes = self.ids.session_name.get_likes()
        LsTab2.dislikes = self.ids.session_name.get_dislikes()

        # Pressing like button caused more likes than dislikes
        index = LsTab2.song_list.find(LsTab2.current_song)
        # Was previously more likes than dislikes
        if LsTab2.song_list[index - 7:index - 1] == "00ff00":
            if LsTab2.likes == LsTab2.dislikes:
                LsTab2.song_list = LsTab2.song_list[:index - 14] + LsTab2.song_list[index:len(LsTab2.song_list) - 8]
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
            elif LsTab2.dislikes > LsTab2.likes:
                LsTab2.song_list = LsTab2.song_list[:index - 7] + "ff0000" + LsTab2.song_list[index - 1:]
                self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})
        # Already had more dislikes than likes
        elif LsTab2.song_list[index - 7:index - 1] == "ff0000":
            return
        # Was even amount of likes and dislikes before pressed
        else:
            LsTab2.song_list = LsTab2.song_list[:index] + "[color=ff0000]" + LsTab2.current_song + "[/color]"
            self.ids.session_name.saved_song.update({'songs_played': LsTab2.song_list})


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
