import kivy
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.database import socket_client
from src.database.socket_client import ListenChat
from src.kv_screens.chat import ChatScreen, show_error

kivy.require('2.3.0')


class LS_Tab1(Screen):
    index = 1
    chat_screen_exists = False

    # self is tab1 screen
    # self.manager is ScreenManager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listener = None
        self.current = None
        self.chat_page = None
        self.background = None
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        sm.ids.chat_screen = None

        self.add_widget(sm)

    def on_enter(self, *args):
        # self has multiple files gathered in arrays, so get only one child
        # make sure you are getting the ScreenManager for session_home and listening_session
        # self.children[0] is currently the ScreenManager for them
        self.ids.session_name = self.manager.ids.session_name
        self.ids.username = self.manager.ids.username

        pass

    def open_dropdown(self, instance):
        dropdown = self.ids.dropdown
        dropdown.open(instance)

    def select_option(self, option):
        print(f'Selected option: {option}')

    def connect(self):
        ip = "spotivibe.net"
        port = 5000
        self.remove_widget(self.ids.add_button)
        if not self.chat_screen_exists:
            self.listener = ListenChat()
            if not self.listener.connect(ip=ip, port=port, my_username=self.ids.username.get_username(),
                                      error_callback=show_error, session_name=self.ids.session_name.get_name()):
                return
            self.chat_page = ChatScreen(self.ids.session_name.get_name(), self.ids.username.get_username(), self.listener)
            self.ids.chat_screen = Screen(name="chat_page", pos_hint={'top': 1})
            self.ids.chat_screen.add_widget(self.chat_page)
            self.add_widget(self.ids.chat_screen)
            self.chat_screen_exists = True
        self.current = 'chat_page'

    def disconnect(self):
        if self.chat_screen_exists:
            self.ids.chat_screen.remove_widget(self.chat_page)
            self.remove_widget(self.ids.chat_screen)
            self.ids.chat_screen = None
            self.chat_screen_exists = False
            self.add_widget(self.ids.add_button)
