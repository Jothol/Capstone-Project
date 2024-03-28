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
    chat_screen_exists = False

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

    # self is home screen
    # self.parent is main.py
    def on_enter(self):
        bl = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        sm.ids = self.parent.ids
        sm.add_widget(Tab1(name='tab1'))
        sm.add_widget(Tab2(name='tab2'))
        sm.add_widget(Tab3(name='tab3'))
        bl.ids = self.parent.ids
        bl.add_widget(sm)
        bl.add_widget(TabBar(self, sm))

        self.add_widget(bl)

    def switch_to(self):
        pass


class TabBar(FloatLayout):

    # self is TabBar object
    # self.screen_manager is ScreenManager for TabBar
    # self.parent is BoxLayout object (child of home screen)
    def __init__(self, home_screen: HomeScreen, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager
        self.screen_manager.ids = home_screen.manager.ids
        self.screen_manager.home_screen = home_screen

    def switch_screen(self, screen_name):
        screen_to_switch = ''

        for i in self.screen_manager.screen_names:
            screen_to_switch = self.screen_manager.get_screen(i)
            if screen_to_switch.index == int(screen_name):
                break

        self.screen_manager.ids = self.screen_manager.parent.ids

        # Determine the direction of the transition
        if screen_to_switch.index > self.screen_manager.current_screen.index:
            direction = 'left'
            direction = 'right'

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_to_switch.name

    def animate_player(self):
        tab_bar = self.ids.tab_bar

        if tab_bar.y < -250:
            animation_window = Animation(pos=(player_window.x, player_window.y + dp(400)), duration=0.1)
        else:
            animation_window = Animation(pos=(player_window.x, player_window.y - dp(400)), duration=0.1)

        animation_window.start(tab_bar)
