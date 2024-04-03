import re

import kivy
from kivy.uix.screenmanager import Screen

from src.database import account as acc

kivy.require('2.3.0')

import time


class AddAccountInfo(Screen):
    def submit(self, email, first_name, last_name):
        if not bool(re.compile(r'[a-zA-Z]*$').match(first_name)):
            self.ids.error_message.text = "Invalid characters in first name."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif not bool(re.compile(r'[a-zA-Z]*$').match(last_name)):
            self.ids.error_message.text = "Invalid characters in last name."
            self.ids.error_message.color = [1, 0, 0, 1]
        else:
            account = self.parent.ids.username
            if email != '':
                account.set_email(email)
            if first_name != '':
                account.set_first_name(first_name)
            if last_name != '':
                account.set_last_name(last_name)
            self.parent.current = 'home_page'
