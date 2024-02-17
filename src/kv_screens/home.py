import kivy
from kivy.uix.screenmanager import Screen

from src.database import account
from src.database.account import Account

kivy.require('2.3.0')


class HomeScreen(Screen):
    username = ''

    def on_enter(self):
        HomeScreen.username = self.parent.ids.username
        first_name = account.get_account(HomeScreen.username).get_first_name()
        self.ids.welcome_label.text = 'Welcome, {}!'.format(first_name)
