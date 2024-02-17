import re

import kivy
from kivy.uix.screenmanager import Screen

from src.database import account as acc

kivy.require('2.3.0')


class AddAccountInfo(Screen):
    def submit(self, email, first_name, last_name):
        if not bool(re.compile(r'[a-zA-Z]+$').match(first_name)):
            self.ids.error_message.text = "Invalid characters in first name."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif not bool(re.compile(r'[a-zA-Z]+$').match(last_name)):
            self.ids.error_message.text = "Invalid characters in last name."
            self.ids.error_message.color = [1, 0, 0, 1]
        else:
            account = acc.get_account(self.parent.ids.username)
            account.set_email(email)
            account.set_first_name(first_name)
            account.set_last_name(last_name)
            self.parent.current = 'home_page'
