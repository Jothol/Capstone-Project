import sys

import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

from src.kv_screens.ls_tab1 import LS_Tab1
from src.kv_screens.ls_tab2 import LS_Tab2
from src.kv_screens.ls_tab3 import LS_Tab3

kivy.require('2.3.0')

from src.database import account
from src.database import session


class ListeningSessionScreen(Screen):
    # self.manager is from main.py
    user = None
    session_name = None

    def on_enter(self, *args):
        bl = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        sm.ids = self.parent.ids
        sm.add_widget(LS_Tab1(name='ls_tab1'))
        sm.add_widget(LS_Tab2(name='ls_tab2'))
        sm.add_widget(LS_Tab3(name='ls_tab3'))
        bl.ids = self.parent.ids
        bl.add_widget(sm)
        bl.add_widget(TabBar(self, sm))
        self.add_widget(bl)

    def on_pre_enter(self, *args):
        sess = self.manager.ids.session_name
        ListeningSessionScreen.user = self.manager.ids.username
        ListeningSessionScreen.session_name = self.manager.ids.session_name
        self.ids.session_label.text = 'Server: {}.'.format(sess.name.id)
        self.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
        print(self.ids)

        # if ListeningSessionScreen.user.username == sess.host.username:
            # print("Hello")
            # bttn = Button(text='hello', size_hint=(None, None))
            # bttn.background_color = [0, 1, 0, 1]
            # bttn.pos_hint = {'x': .5, 'y': .5}
            #
            # self.add_widget(bttn)
        pass

    def add_account(self):
        sess = self.manager.ids.session_name
        user = self.manager.ids.username
        if sess.host.username != user.username:
            print("Only host can add users")
            self.ids.error_message.color = [1, 0, 0, 1]
        pass

    def submit(self):
        sess = self.manager.ids.session_name
        user = self.manager.ids.username
        if sess.host.username == user.username:
            sess.remove_host()
        else:
            sess.remove_user(user)

        self.parent.ids.session_name = None
        self.manager.current = "home_page"


class TabBar(FloatLayout):

    # self is TabBar object
    # self.screen_manager is ScreenManager for TabBar
    # self.parent is BoxLayout object (child of home screen)
    def __init__(self, ls_screen: ListeningSessionScreen, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager
        self.screen_manager.ids = ls_screen.ids
        self.screen_manager.ls_screen = ls_screen
        # self.screen_manager.home = home

    def switch_screen(self, screen_name):
        # Access the ScreenManager and switch to the desired screen
        screen_to_switch = ''

        for i in self.screen_manager.screen_names:
            screen_to_switch = self.screen_manager.get_screen(i)
            if screen_to_switch.index == int(screen_name):
                break

        self.screen_manager.ids = self.screen_manager.parent.ids

        # Determine the direction of the transition
        if screen_to_switch.index > self.screen_manager.current_screen.index:
            direction = 'left'
        else:
            direction = 'right'

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_to_switch.name
