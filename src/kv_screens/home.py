import sys

import kivy
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from src.database import account, socket_client
from src.database.account import Account
from src.kv_screens.chat import ChatScreen

kivy.require('2.3.0')


def show_error(message):
    print(message)
    Clock.schedule_once(sys.exit, 10)


class HomeScreen(Screen):
    username = ''

    def on_enter(self):
        HomeScreen.username = self.parent.ids.username
        first_name = account.get_account(HomeScreen.username).get_first_name()
        if first_name != '':
            self.ids.welcome_label.text = 'Welcome, {}!'.format(first_name)

    def connect(self):
        ip = "127.0.0.1"
        port = 5000
        if not socket_client.connect(ip, port, self.parent.ids.username, show_error):
            return
        self.chat_page = ChatScreen()
        screen = Screen(name="chat_page")
        screen.add_widget(self.chat_page)
        self.parent.add_widget(screen)
        self.parent.current = 'chat_page'
