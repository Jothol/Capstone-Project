import kivy
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager

from src.database import account
from src.database import session

kivy.require('2.3.0')


class LS_Tab3(Screen):
    index = 3
    user = None
    session_name = None
    add_button_layout = None
    remove_button_layout = None
    user_list = None

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

    def on_enter(self, *args):
        LS_Tab3.user_list = self.manager.parent.parent.user_list
        user_str = ""
        print(LS_Tab3.user_list)
        for i in LS_Tab3.user_list:
            if user_str == "":
                user_str = i
            else:
                user_str += ", " + i
        print("user_array", user_str)
        self.ids.accs_list.text = user_str

    def submit(self):
        sess = self.manager.ids.session_name
        user = self.manager.ids.username
        # Clock.unschedule(self.host_replacement)
        if sess.host.username == user.username:
            sess.remove_host()
            # self.remove_widget(LS_Tab3.host_bar)
            # cLS_Tab3.host_bar = None
        else:
            sess.remove_user(user)
