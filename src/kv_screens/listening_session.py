import sys

import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.graphics import Color, Rectangle

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
    host_bar = None
    add_button_layout = None
    remove_button_layout = None
    new_host_button_layout = None

    def on_enter(self, *args):
        bl = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        sm.ids = self.parent.ids
        sm.add_widget(LS_Tab1(name='ls_tab1'))
        sm.add_widget(LS_Tab2(name='ls_tab2'))
        sm.add_widget(LS_Tab3(name='ls_tab3'))
        bl.ids = self.parent.ids
        bl.add_widget(sm)
        bl.add_widget(TabBar2(self, sm))
        self.add_widget(bl)

        if ListeningSessionScreen.user.username == self.manager.ids.session_name.host.username:
            bl2 = BoxLayout(orientation='horizontal', size_hint=(.4, .1), size=(200, 20),
                            pos_hint={'center_x': .5, 'center_y': 1})
            bl2.ids = self.parent.ids
            bl2.canvas.before.add(Color(0.1, 0.1, 0.1, 1))
            bl2.canvas.before.add(Rectangle(size=(1200, 50), pos=(0, 850)))
            bl2.add_widget(Button(text='Add User', background_color=[0, 1, 0, 1], size_hint=(.5, .5),
                                  pos=(600, 850), size=(130, 30), on_press=self.open_add_user))
            bl2.add_widget(Button(text='Remove User', background_color=[0, 1, 0, 1], size_hint=(.5, .5),
                                  pos=(600, 850), size=(130, 30), on_press=self.open_remove_user))
            bl2.add_widget(Button(text='New Host', background_color=[0, 1, 0, 1], size_hint=(.5, .5),
                                  pos=(600, 850), size=(130, 30), on_press=self.open_new_host))
            self.add_widget(bl2)
            ListeningSessionScreen.host_bar = bl2

    def on_pre_enter(self, *args):
        sess = self.manager.ids.session_name
        ListeningSessionScreen.user = self.manager.ids.username
        ListeningSessionScreen.session_name = self.manager.ids.session_name
        self.ids.session_label.text = 'Server: {}.'.format(sess.name.id)
        self.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)

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
            self.remove_widget(ListeningSessionScreen.host_bar)
            ListeningSessionScreen.host_bar = None
        else:
            sess.remove_user(user)
        if self.children[0].children[1].current is "ls_tab2":
            Clock.unschedule(LS_Tab2.get_current_song)
            # TODO fix this as it does not currently work
        self.parent.ids.session_name = None
        self.manager.current = "home_page"

    def open_add_user(self, instance):
        sess = ListeningSessionScreen.session_name
        user = ListeningSessionScreen.user
        if sess.host.username != user.username:
            print("Only host can add users")
            return
        if ListeningSessionScreen.add_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.add_button_layout)
            ListeningSessionScreen.add_button_layout = None
            return
        if ListeningSessionScreen.remove_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.remove_button_layout)
            ListeningSessionScreen.remove_button_layout = None
        if ListeningSessionScreen.new_host_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.new_host_button_layout)
            ListeningSessionScreen.new_host_button_layout = None

        bl = BoxLayout(orientation="horizontal", size_hint=(.4, .070), size=(100, 60),
                       pos=(350, 795))
        bl.padding = 10
        bl.canvas.before.add(Color(0.2, 0.2, 0.2, 1))
        bl.canvas.before.add(Rectangle(size=(500, 50), pos=(350, 800)))
        bl.add_widget(Label(text='Insert name:', color=[1, 1, 1, 1], bold=True, size_hint=(.35, 1)))
        bl.add_widget(TextInput(multiline=False, hint_text='Add User', size_hint=(.50, 1)))
        bl.add_widget(Button(text='Enter', background_color=[0, 1, 0, 1], size_hint=(.15, 1), pos_hint={'center_x': .5},
                             on_press=self.add_acc))
        ListeningSessionScreen.add_button_layout = bl
        self.add_widget(bl)

    def add_acc(self, instance):
        user_name = ListeningSessionScreen.add_button_layout.children[1].text
        user = account.get_account(user_name)
        if user is None:
            print("User not found")
        else:
            print("user found!")
            ListeningSessionScreen.session_name.add_user(user)
        pass

    def open_remove_user(self, instance):
        sess = ListeningSessionScreen.session_name
        user = ListeningSessionScreen.user
        if sess.host.username != user.username:
            print("Only host can add users")
            return
        if ListeningSessionScreen.remove_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.remove_button_layout)
            ListeningSessionScreen.remove_button_layout = None
            return
        if ListeningSessionScreen.add_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.add_button_layout)
            ListeningSessionScreen.add_button_layout = None
        if ListeningSessionScreen.new_host_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.new_host_button_layout)
            ListeningSessionScreen.new_host_button_layout = None

        bl = BoxLayout(orientation="horizontal", size_hint=(.4, .070), size=(100, 60),
                       pos=(350, 795))
        bl.padding = 10
        bl.canvas.before.add(Color(0.2, 0.2, 0.2, 1))
        bl.canvas.before.add(Rectangle(size=(500, 50), pos=(350, 800)))
        bl.add_widget(Label(text='Insert name:', color=[1, 1, 1, 1], bold=True, size_hint=(.35, 1)))
        bl.add_widget(TextInput(multiline=False, hint_text='Remove User', size_hint=(.50, 1)))
        bl.add_widget(Button(text='Enter', background_color=[0, 1, 0, 1], size_hint=(.15, 1), pos_hint={'center_x': .5},
                             on_press=self.remove_acc))
        ListeningSessionScreen.remove_button_layout = bl
        self.add_widget(bl)

    def remove_acc(self, instance):
        user_name = ListeningSessionScreen.remove_button_layout.children[1].text
        user = account.get_account(user_name)
        if session.get_user(ListeningSessionScreen.session_name.name, user_name) is None:
            print("User not found")
        else:
            print("user found!")
            ListeningSessionScreen.session_name.remove_user(user)
        pass

    def open_new_host(self, instance):
        sess = ListeningSessionScreen.session_name
        user = ListeningSessionScreen.user
        if sess.host.username != user.username:
            print("Only host can add users")
            return
        if ListeningSessionScreen.new_host_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.new_host_button_layout)
            ListeningSessionScreen.new_host_button_layout = None
            return
        if ListeningSessionScreen.add_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.add_button_layout)
            ListeningSessionScreen.add_button_layout = None
        if ListeningSessionScreen.remove_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.remove_button_layout)
            ListeningSessionScreen.remove_button_layout = None

        bl = BoxLayout(orientation="horizontal", size_hint=(.4, .070), size=(100, 60),
                       pos=(350, 795))
        bl.padding = 10
        bl.canvas.before.add(Color(0.2, 0.2, 0.2, 1))
        bl.canvas.before.add(Rectangle(size=(500, 50), pos=(350, 800)))
        bl.add_widget(Label(text='Insert name:', color=[1, 1, 1, 1], bold=True, size_hint=(.35, 1)))
        bl.add_widget(TextInput(multiline=False, hint_text='New Host', size_hint=(.50, 1)))
        bl.add_widget(Button(text='Enter', background_color=[0, 1, 0, 1], size_hint=(.15, 1), pos_hint={'center_x': .5},
                             on_press=self.new_host))
        ListeningSessionScreen.new_host_button_layout = bl
        self.add_widget(bl)
        print(ListeningSessionScreen.new_host_button_layout.children)

        pass

    def new_host(self, instance):
        user_name = ListeningSessionScreen.new_host_button_layout.children[1].text
        user = account.get_account(user_name)
        if session.get_user(ListeningSessionScreen.session_name.name, user_name) is None:
            print("User not found")
        print("user found!")
        ListeningSessionScreen.session_name.name.update({ListeningSessionScreen.user.username: 'user'})
        ListeningSessionScreen.session_name.name.update({user_name: 'host'})
        ListeningSessionScreen.session_name.host = user
        self.remove_widget(ListeningSessionScreen.host_bar)
        self.remove_widget(ListeningSessionScreen.new_host_button_layout)
        ListeningSessionScreen.host_bar = None
        ListeningSessionScreen.new_host_button_layout = None
        self.ids.user_label.text = 'Hosted by: {}.'.format(ListeningSessionScreen.session_name.host.username)


class TabBar2(FloatLayout):

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
