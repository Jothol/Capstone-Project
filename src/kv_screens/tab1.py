import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

# from src.kv_screens.session_home import SessionHomeScreen

kivy.require('2.3.0')


class Tab1(Screen):
    index = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(SessionHomeScreen(name='session_home_page'))

    def open_dropdown(self, instance):
        dropdown = self.ids.dropdown
        dropdown.open(instance)

    def select_option(self, option):
        print(f'Selected option: {option}')
