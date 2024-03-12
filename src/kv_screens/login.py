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
            acc = account.get_account(username)
            self.parent.ids.username = acc
            self.parent.current = "home_page"

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # Enter key
            self.send_message(None)
