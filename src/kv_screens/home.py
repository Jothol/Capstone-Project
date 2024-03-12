import sys

import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition


from src.database import account, socket_client
from src.database.account import Account
from src.kv_screens.chat import ChatScreen
from src.kv_screens.tab1 import Tab1
from src.kv_screens.tab2 import Tab2
from src.kv_screens.tab3 import Tab3

kivy.require('2.3.0')


def show_error(message):
    print(message)
    Clock.schedule_once(sys.exit, 10)


class HomeScreen(Screen):
    username = ''
    chat_screen_exists = False

    def on_enter(self):
        HomeScreen.username = self.parent.ids.username
        first_name = account.get_account(HomeScreen.username).get_first_name()
        if first_name != '':
            self.ids.welcome_label.text = 'Welcome, {}!'.format(first_name)

    def connect(self):
        ip = "spotivibe.net"
        port = 5000
        if not self.chat_screen_exists:
            if not socket_client.connect(ip, port, self.parent.ids.username, show_error):
                return
            self.chat_page = ChatScreen()
            screen = Screen(name="chat_page")
            screen.add_widget(self.chat_page)
            self.parent.add_widget(screen)
            self.chat_screen_exists = True
        self.parent.current = 'chat_page'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bl = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        sm.add_widget(Tab1(name='tab1'))
        sm.add_widget(Tab2(name='tab2'))
        sm.add_widget(Tab3(name='tab3'))
        bl.add_widget(sm)
        bl.add_widget(TabBar(sm))
        self.add_widget(bl)


class TabBar(FloatLayout):

    def __init__(self, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager

    def switch_screen(self, screen_name):
        # Access the ScreenManager and switch to the desired screen
        screen_to_switch = self.screen_manager.get_screen(screen_name)

        # Determine the direction of the transition
        if screen_to_switch.index > self.screen_manager.current_screen.index:
            direction = 'left'
        else:
            direction = 'right'

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_name
