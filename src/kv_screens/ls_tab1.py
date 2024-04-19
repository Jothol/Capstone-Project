import random

import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock

from src.database import socket_client
from src.kv_screens.chat import ChatScreen, show_error

kivy.require('2.3.0')


class LS_Tab1(Screen):
    index = 1
    chat_screen_exists = False
    close = False
    background_image = None
    float_image = None

    # self is tab1 screen
    # self.manager is ScreenManager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create background image but do not add until welcome message is displayed
        self.float_image = FloatLayout(size=(Window.width, Window.height))
        self.background_image = Image(source='../other/images/transparent_logo.png', fit_mode='scale-down',
                                      opacity=0)
        self.float_image.add_widget(self.background_image)
        self.add_widget(self.float_image)


        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None

        self.add_widget(sm)



    def on_enter(self, *args):
        # self has multiple files gathered in arrays, so get only one child
        # make sure you are getting the ScreenManager for session_home and listening_session
        # self.children[0] is currently the ScreenManager for them
        self.ids.session_name = self.manager.ids.session_name
        self.ids.username = self.manager.ids.username
        if LS_Tab1.close is False:
            self.ids.welcome_label.text = "Welcome to " + self.ids.session_name.name.id + ", {}!".format(
                self.ids.username.username)

        Clock.schedule_interval(self.welcome, 3)

    def welcome(self, instance):
        self.ids.welcome_label.text = ""
        LS_Tab1.close = True
        self.background_image.opacity = 1
        Clock.unschedule(self.welcome)

    def open_dropdown(self, instance):
        dropdown = self.ids.dropdown
        dropdown.open(instance)

    def select_option(self, option):
        print(f'Selected option: {option}')

    def connect(self):
        ip = "spotivibe.net"
        port = 5000
        self.remove_widget(self.ids.add_button)
        self.remove_widget(self.float_image)
        colors = ["dd2020", "00ff00", "ffff00", "00ffff", "8a2be2", "ff00ff", "ffa500"]
        if not self.chat_screen_exists:
            color = random.choice(colors)
            if not socket_client.connect(ip, port, self.ids.username.get_username(), show_error,
                                         self.ids.session_name.get_name(), color):
                return
            self.chat_page = ChatScreen(self.ids.session_name.get_name(), self.ids.username.get_username(), color)
            self.screen = Screen(name="chat_page")
            self.screen.add_widget(self.chat_page)
            self.add_widget(self.screen)
            self.chat_screen_exists = True
        self.current = 'chat_page'

    def disconnect(self):
        if self.chat_screen_exists:
            self.add_widget(self.ids.add_button)
            self.add_widget(self.float_image)
            self.screen.clear_widgets()
            self.remove_widget(self.screen)
            self.chat_screen_exists = False
