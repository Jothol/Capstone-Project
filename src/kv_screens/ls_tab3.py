import kivy
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

from src.database import account
from src.database import session

from src.kv_screens import player

kivy.require('2.3.0')

sp = player.sp


class LS_Tab3(Screen):
    index = 3
    user = None
    session_name = None
    add_button_layout = None
    remove_button_layout = None
    user_list = None
    song_list = ""
    current_song = None
    error_window_open = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="LS_Tab 3!"))
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        self.add_widget(sm)

    def on_pre_enter(self, *args):
        LS_Tab3.user = self.manager.ids.username
        LS_Tab3.session_name = self.manager.ids.session_name
        LS_Tab3.user_list = self.manager.parent.parent.user_list
        user_str = ""
        for i in LS_Tab3.user_list:
            if user_str == "":
                user_str = i
            else:
                user_str += ", " + i
        self.ids.accs_list.text = user_str
        self.ids.song_info.text = LS_Tab3.session_name.saved_song.get().get('songs_played')

    def on_enter(self, *args):
        self.ids.session_name = self.manager.ids.session_name
        self.ids.username = self.manager.ids.username

        Clock.schedule_interval(self.refresh_settings, 1.5)

    def on_leave(self, *args):
        Clock.unschedule(self.refresh_settings)
        pass

    def refresh_settings(self, instance):
        print("Testing: ", self.ids.session_name.host)
        user_str = ""
        LS_Tab3.user_list = self.manager.parent.parent.user_list
        for i in LS_Tab3.user_list:
            if user_str == "":
                user_str = i
            else:
                user_str += ", " + i
        print("user_array", user_str)
        self.ids.accs_list.text = user_str
        self.ids.song_info.text = LS_Tab3.session_name.saved_song.get().get('songs_played')

    def submit(self):
        sess = LS_Tab3.session_name
        print("sess", sess)
        print("host", sess.host)
        user = self.manager.ids.username
        print(self.manager.screen_names)
        if sess.host.username == user.username:
            sess.remove_host()
            # self.remove_widget(LS_Tab3.host_bar)
            # cLS_Tab3.host_bar = None
        else:
            sess.remove_user(user)

        self.manager.ls_screen.manager.current = "home_page"
        Clock.unschedule(self.refresh_settings)

    def send_friend_request(self, user_name):
        acc = session.get_user(LS_Tab3.session_name.name, user_name)
        if self.error_window_open:
            return False
        if acc is None:
            self.animate_error_window('User not found in session.', (1, 0, 0, 1))
            return False
        elif user_name in LS_Tab3.user.friends:
            self.animate_error_window('Already friends with ' + user_name + '.', (1, 0, 0, 1))
            return False
        elif LS_Tab3.user.username in acc.friends:
            self.animate_error_window('Already sent a request to ' + user_name + '.', (1, 0, 0, 1))
        self.animate_error_window('Friend request sent to ' + user_name + '.', (0, 0.5, 0, 1))
        LS_Tab3.user.send_invite(user_name)
        if acc.username in LS_Tab3.user.get_invites():
            LS_Tab3.user.add_friend(acc.username)
            acc.add_friend(LS_Tab3.user.username)
            LS_Tab3.user.delete_invite(acc.username)
            acc.delete_invite(LS_Tab3.user.username)
        return True

    def animate_error_window(self, message: str, color):
        error_window = self.ids.error_window
        message_label = self.ids.window_message
        if message != '':
            message_label.text = message
            error_window.x = dp(-200)
        if error_window.x <= dp(-7):
            self.ids.friend_input.text = ''
            self.error_window_open = True
            animation_window = Animation(pos=(error_window.x + dp(195), error_window.y), duration=0.1)
            error_window.opacity = 1
            message_label.color = color
            animation_window.start(error_window)
            Clock.schedule_once(lambda dt: self.animate_error_window('', (0, 0, 0, 0)), 5)
        else:
            self.error_window_open = False
            animation_window = Animation(pos=(error_window.x - dp(195), error_window.y), duration=0.1)
            animation_window.start(error_window)
            animation_window.bind(on_complete=lambda *args: setattr(error_window, 'opacity', 0))
            animation_window.bind(on_complete=lambda *args: setattr(message_label, 'text', ''))