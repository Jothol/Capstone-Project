import kivy
from kivy.uix.screenmanager import Screen
import re

kivy.require('2.3.0')

import src.database.account as account


class CreateAccount(Screen):
    def submit(self, username, password, re_password):
        if password != re_password:
            self.ids.error_message.text = "Passwords do not match."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif password == "":
            self.ids.error_message.text = "Password cannot be blank."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif len(username) > 10:
            self.ids.error_message.text = "Username too long."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif len(password) > 20:
            self.ids.error_message.text = "Password too long."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif not bool(re.compile(r'[a-zA-Z0-9]+$').match(username)):
            self.ids.error_message.text = "Invalid characters in username."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif account.create_account(username=username, password=password) is None:
            self.ids.error_message.text = "Username taken."
            self.ids.error_message.color = [1, 0, 0, 1]
        else:
            self.parent.ids.username = account.get_account(username)
            self.parent.current = 'add_account_info_page'
