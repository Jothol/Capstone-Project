import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image

from src.database import socket_client
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
        self.background_image = Image(source='../other/images/transparent_logo.png', fit_mode='scale-down')
        self.float_image = FloatLayout(size=(Window.width, Window.height))
        self.float_image.add_widget(self.background_image)

        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None

        self.add_widget(self.float_image)
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
        self.remove_widget(self.float_image)
        if not self.chat_screen_exists:
            if not socket_client.connect(ip, port, self.ids.username.get_username(), show_error, self.ids.session_name.get_name()):
                return
            self.chat_page = ChatScreen(self.ids.session_name.get_name(), self.ids.username.get_username())
            self.chat_page.leave_chat.bind(on_press=lambda instance: self.disconnect())
            self.screen = Screen(name="chat_page")
            self.screen.add_widget(self.chat_page)
            self.add_widget(self.screen)
            self.chat_screen_exists = True
        self.current = 'chat_page'

    def disconnect(self):
        if self.chat_screen_exists:
            self.add_widget(self.ids.add_button)
            self.add_widget(self.float_image)
            self.screen.remove_widget(self.chat_page)
            self.remove_widget(self.screen)
            self.chat_screen_exists = False
