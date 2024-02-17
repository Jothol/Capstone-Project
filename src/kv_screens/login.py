import kivy
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')

from src.database import account


class LoginScreen(Screen):

    def submit(self, username, password):
        if not account.try_login(username, password):
            self.ids.error_message.text = "Username or password incorrect."
            self.ids.error_message.color = [1, 0, 0, 1]
        else:
            self.parent.ids.username = username
            self.parent.current = "home_page"