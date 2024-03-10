import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.kv_screens.session_home import SessionHomeScreen

from src.kv_screens.listening_session import ListeningSessionScreen

kivy.require('2.3.0')


class Tab1(Screen):
    index = 1

    # self is tab1 screen
    # self.manager is screenmanager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = ''
        sm.ids.session_name = ''
        sm.add_widget(SessionHomeScreen(name='session_home_page'))
        sm.add_widget(ListeningSessionScreen(name='listening_session_page'))
        self.add_widget(sm)

    def on_enter(self, *args):
        print(self)
        self.children[0].ids = self.manager.ids  # self.children[0] must be ScreenManager
        print(self.manager.ids)
        pass

    def open_dropdown(self, instance):
        dropdown = self.ids.dropdown
        dropdown.open(instance)

    def select_option(self, option):
        print(f'Selected option: {option}')
