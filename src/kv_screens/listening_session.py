import kivy
from kivy.uix.screenmanager import Screen

from src.database import account
from src.database import session

kivy.require('2.3.0')


class ListeningSessionScreen(Screen):
    def on_enter(self):
        print("Hello world")
