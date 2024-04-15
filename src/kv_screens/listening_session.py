import sys

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp

from src.kv_screens.ls_tab1 import LS_Tab1
from src.kv_screens.ls_tab2 import LS_Tab2
from src.kv_screens.ls_tab3 import LS_Tab3

kivy.require('2.3.0')

from src.database import account
from src.database import session


def set_opacity(image: Image, opacity):
    # Find the Color instruction in canvas.after
    for instruction in image.canvas.after.children:
        if isinstance(instruction, Color):
            # Modify the opacity value
            instruction.rgba = (instruction.rgba[0], instruction.rgba[1], instruction.rgba[2], opacity)
            break


class ListeningSessionScreen(Screen):
    # self.manager is from main.py
    user = None  # Account object of current user
    session_name = None  # Session object of listening session
    host_box_layout = None  # the boxlayout of host permissions created in on_enter
    host_bar = None  # Used to show or hide the host_bar depending on the user
    add_button_layout = None  # layout for inviting user
    remove_button_layout = None  # layout for removing user
    new_host_button_layout = None  # layout for replacing host
    end_session_button_layout = None  # layout for ending session
    screen_manager = None  # helper created for removing hostbar on ls_tab3
    user_list = None
    status = "Private"
    the_host_bar = None

    def on_enter(self, *args):
        ListeningSessionScreen.session_name.name = (
            self.parent.ids.session_name.db.collection('sessions').document(self.parent.ids.session_name.name.id))
        bl = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        sm.ids = self.parent.ids
        sm.add_widget(LS_Tab1(name='ls_tab1'))
        sm.add_widget(LS_Tab2(name='ls_tab2'))
        sm.add_widget(LS_Tab3(name='ls_tab3'))
        ListeningSessionScreen.screen_manager = sm
        bl.ids = self.parent.ids
        bl.add_widget(sm)
        bl.add_widget(TabBar2(self, sm))
        self.add_widget(bl)
        ListeningSessionScreen.the_host_bar = HostBar(self, sm)
        if ListeningSessionScreen.user.username == self.manager.ids.session_name.host.username:
            self.add_widget(ListeningSessionScreen.the_host_bar)
            ListeningSessionScreen.host_bar = ListeningSessionScreen.the_host_bar

        Clock.schedule_interval(self.session_refresher, 1.3)

    def on_pre_enter(self, *args):
        sess = self.manager.ids.session_name
        ListeningSessionScreen.user = self.manager.ids.username
        ListeningSessionScreen.session_name = self.manager.ids.session_name
        ListeningSessionScreen.user_list = sess.name.get().to_dict()
        if sess and sess.name:
            self.ids.session_label.text = 'Server: {}.'.format(sess.name.id)
        else:
            self.ids.session_label.text = 'Server: Unknown.'
        if sess and sess.host:
            self.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
        else:
            self.ids.user_label.text = 'Hosted by: Unknown.'

        pass

    def on_leave(self, *args):
        Clock.unschedule(self.session_refresher)

    # Method process of User leaving session and back to home screen
    def submit(self):
        sess = self.manager.ids.session_name
        user = self.manager.ids.username
        # Clock.unschedule(self.host_replacement)
        if sess.host.username == user.username:
            sess.remove_host()
            self.remove_widget(ListeningSessionScreen.host_bar)
            ListeningSessionScreen.host_bar = None
        else:
            sess.remove_user(user)
        if self.children[0].children[1].current is "ls_tab2":
            self.children[0].children[1].current = "ls_tab1"
        self.parent.ids.session_name = None
        self.parent.ids.username.in_session = False
        self.manager.current = "home_page"

    # BEGINNING OF CLOCK METHOD
    def session_refresher(self, instance):
        sess = ListeningSessionScreen.session_name
        acc = ListeningSessionScreen.user
        ListeningSessionScreen.user_list = data = sess.name.get().to_dict()
        if data is None:  # session ended and user goes back to home page
            self.parent.ids.session_name = None
            self.manager.current = "home_page"
            self.parent.ids.username.in_session = False
        elif acc.username not in data:  # user got kicked from session and goes to home page
            self.parent.ids.session_name = None
            self.manager.current = "home_page"
            self.parent.ids.username.in_session = False
        elif data.get(acc.username) == "host":  # decides when host sees host bar
            if ListeningSessionScreen.host_bar is None:
                sess.host = acc  # update in case acc just became new host
                if ListeningSessionScreen.screen_manager.current != "ls_tab3":
                    ListeningSessionScreen.host_bar = ListeningSessionScreen.the_host_bar
                    self.add_widget(ListeningSessionScreen.host_bar)
                    self.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
            else:
                if ListeningSessionScreen.screen_manager.current == "ls_tab3":
                    self.remove_widget(ListeningSessionScreen.host_bar)
                    ListeningSessionScreen.host_bar = None

    # END OF CLOCK METHOD

    # BEGINNING OF HOST BUTTON METHODS
    # BEGINNING OF END SESSION BUTTON
    def end_session(self, instance):
        Clock.unschedule(self.session_refresher)
        # Clock.unschedule(self.host_replacement)
        self.parent.ids.session_name = None
        self.manager.current = "home_page"
        self.remove_widget(ListeningSessionScreen.end_session_button_layout)
        # Clock.unschedule(self.host_replacement)
        ListeningSessionScreen.end_session_button_layout = None
        for col in ListeningSessionScreen.session_name.name.collections():
            for doc in col.list_documents():
                doc.delete()
        user_list = ListeningSessionScreen.session_name.name.get().to_dict()
        while user_list.__len__() > 0:
            temp = user_list.popitem()
            acc = account.get_account(temp[0])
            acc.account.update({'in_session': False})
            acc.in_session = False

        self.parent.ids.username.in_session = False
        ListeningSessionScreen.session_name.name.delete()  # actual deletion of session name in firebase

    def cancel_end_session_request(self, instance):
        self.remove_widget(ListeningSessionScreen.end_session_button_layout)
        ListeningSessionScreen.end_session_button_layout = None

    def open_end_session(self, instance):
        sess = ListeningSessionScreen.session_name
        user = ListeningSessionScreen.user
        if sess.host.username != user.username:
            print("Only host can add users")
            return
        if ListeningSessionScreen.end_session_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.end_session_button_layout)
            ListeningSessionScreen.end_session_button_layout = None
            return
        if ListeningSessionScreen.add_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.add_button_layout)
            ListeningSessionScreen.add_button_layout = None
        if ListeningSessionScreen.remove_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.remove_button_layout)
            ListeningSessionScreen.remove_button_layout = None
        if ListeningSessionScreen.new_host_button_layout is not None:
            self.remove_widget(ListeningSessionScreen.new_host_button_layout)
            ListeningSessionScreen.new_host_button_layout = None

        bl = BoxLayout(orientation="horizontal", size_hint=(.25, .070), size=(100, 60),
                       pos=(450, 795))
        bl.padding = 10
        bl.canvas.before.add(Color(0.2, 0.2, 0.2, 1))
        bl.canvas.before.add(Rectangle(size=(285, 50), pos=(465, 800)))
        bl.add_widget(Label(text='Are you sure?', color=[1, 1, 1, 1], bold=True, size_hint=(.60, 1)))
        bl.add_widget(Button(text='Yes', background_color=[0, 1, 0, 1], size_hint=(.2, .8),
                             pos_hint={'center_x': .5, 'center_y': .5}, on_press=self.end_session))
        bl.add_widget(Button(text='No', background_color=[0, 1, 0, 1], size_hint=(.2, .8),
                             pos_hint={'center_x': .5, 'center_y': .5}, on_press=self.cancel_end_session_request))
        ListeningSessionScreen.end_session_button_layout = bl
        self.add_widget(bl)
    # END OF END SESSION BUTTON
    # END OF HOST BUTTON METHODS


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
        print(self.screen_manager.current)
        # Access the ScreenManager and switch to the desired screen
        screen_to_switch = ''

        set_opacity(self.ids.chat_image, 0)
        set_opacity(self.ids.music_image, 0)
        set_opacity(self.ids.settings_image, 0)

        if int(screen_name) == 1:
            set_opacity(self.ids.chat_image, 0.5)
            Animation(size=(self.ids.chat_button.width * 0.8, self.ids.chat_button.height * 0.8),
                      center=self.ids.chat_button.center, duration=0.1).start(self.ids.chat_image)
        elif int(screen_name) == 2:
            set_opacity(self.ids.music_image, 0.5)
            Animation(size=(self.ids.music_button.width * 0.7, self.ids.music_button.height * 0.7),
                      center=self.ids.music_button.center, duration=0.1).start(self.ids.music_image)
        else:
            set_opacity(self.ids.settings_image, 0.5)
            Animation(size=(self.ids.setting_button.width * 0.7, self.ids.setting_button.height * 0.7),
                      center=self.ids.setting_button.center, duration=0.1).start(self.ids.settings_image)

        for i in self.screen_manager.screen_names:
            screen_to_switch = self.screen_manager.get_screen(i)
            if screen_to_switch.index == int(screen_name):
                break

        if self.screen_manager.current == 'ls_tab3' and int(screen_name) != 3:
            Animation(size=(self.ids.setting_button.width * 0.5, self.ids.setting_button.height * 0.5),
                      center=self.ids.setting_button.center, duration=0.1).start(self.ids.settings_image)
        elif self.screen_manager.current == 'ls_tab2' and int(screen_name) != 2:
            Animation(size=(self.ids.music_button.width * 0.5, self.ids.music_button.height * 0.5),
                      center=self.ids.music_button.center, duration=0.1).start(self.ids.music_image)
        elif self.screen_manager.current == 'ls_tab1' and int(screen_name) != 1:
            Animation(size=(self.ids.chat_button.width * 0.6, self.ids.chat_button.height * 0.6),
                      center=self.ids.chat_button.center, duration=0.1).start(self.ids.chat_image)

        self.screen_manager.ids = self.screen_manager.parent.ids

        # Determine the direction of the transition
        if screen_to_switch.index > self.screen_manager.current_screen.index:
            direction = 'left'
        else:
            direction = 'right'

        if int(screen_name) == 3:
            if ListeningSessionScreen.host_bar is not None:
                self.screen_manager.ls_screen.remove_widget(ListeningSessionScreen.host_bar)
                ListeningSessionScreen.host_bar = None

        acc_username = self.screen_manager.ls_screen.user.username
        host_username = self.screen_manager.ls_screen.session_name.host.username
        if self.screen_manager.current_screen.name == "ls_tab3":
            if host_username == acc_username:
                ListeningSessionScreen.host_bar = ListeningSessionScreen.the_host_bar
                self.screen_manager.ls_screen.add_widget(ListeningSessionScreen.host_bar)

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_to_switch.name


class HostBar(BoxLayout):
    on_open = False
    drop_down = None
    input_text = ""
    def __init__(self, ls_screen: ListeningSessionScreen, screen_manager: ScreenManager, **kwargs):
        super(HostBar, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.screen_manager.ids = ls_screen.parent.ids
        self.screen_manager.ls_screen = ls_screen

    def change_status(self):
        if self.ids.status.text == "Private":
            self.ids.status.text = "Public"
            self.ids.status.background_color = [0, 1, 0.6, 1]
            # self.parent.ids.session_name.session_status.update({'status': 'public'})
            print(self.screen_manager.ls_screen.ids)
            print(self.screen_manager.ls_screen.parent.ids)
            print(self.screen_manager.parent.ids)
            print(self.screen_manager.ids.session_name)
            self.screen_manager.ids.session_name.session_status.update({'status': 'public'})
        else:
            self.ids.status.text = "Private"
            self.ids.status.background_color = [1, 0, 0.4, 1]
            # self.parent.ids.session_name.session_status.update({'status': 'private'})
            self.screen_manager.ids.session_name.session_status.update({'status': 'private'})

    def open_bar(self, input_text):
        if HostBar.on_open is False:
            HostBar.drop_down = HostDropBar(self.screen_manager.ls_screen, self.screen_manager)
            self.screen_manager.ls_screen.add_widget(HostBar.drop_down)
            HostBar.on_open = True
            HostBar.input_text = input_text
            if input_text == "Invite User":
                HostBar.drop_down.ids.input_label.text = "Enter invited user:"
            elif input_text == "Remove User":
                HostBar.drop_down.ids.input_label.text = "Enter removed user:"
            elif input_text == "New Host":
                HostBar.drop_down.ids.input_label.text = "Enter new host:"
        else:
            if HostBar.input_text == input_text:
                self.screen_manager.ls_screen.remove_widget(HostBar.drop_down)
                HostBar.on_open = False
                HostBar.drop_down = None
            else:
                HostBar.input_text = input_text
                if input_text == "Invite User":
                    HostBar.drop_down.ids.input_label.text = "Enter invited user:"
                elif input_text == "Remove User":
                    HostBar.drop_down.ids.input_label.text = "Enter removed user:"
                elif input_text == "New Host":
                    HostBar.drop_down.ids.input_label.text = "Enter new host:"


class HostDropBar(BoxLayout):

    def __init__(self, ls_screen: ListeningSessionScreen, screen_manager: ScreenManager, **kwargs):
        super(HostDropBar, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.screen_manager.ids = ls_screen.parent.ids
        self.screen_manager.ls_screen = ls_screen

    def submit(self, user_name):
        if user_name == "":
            print("Must enter valid name")
            return

        user = account.get_account(user_name)
        sess = ListeningSessionScreen.session_name
        print("username", user_name)
        if self.ids.input_label.text == "Enter invited user:":
            if user is None:
                print("User not found")
            else:
                try:
                    index = user.friends.index(sess.host.username)
                    if sess.name.id in user.session_invites:
                        print("User already received pended invite")
                    else:
                        user.session_invites.append(sess.name.id)
                        user.account.update({'session_invites': user.session_invites})
                except ValueError:
                    print("You are not friends with the user")
                    return
        elif self.ids.input_label.text == "Enter removed user:":
            if session.get_user(sess.name, user_name) is None:
                print("User not found")
            else:
                print("user found!")
                sess.remove_user(user)
        elif self.ids.input_label.text == "Enter new host:":
            if session.get_user(sess.name, user_name) is None:
                print("User not found")
                return
            sess.name.update({ListeningSessionScreen.user.username: 'user'})
            sess.name.update({user_name: 'host'})
            sess.host = user
            self.screen_manager.ls_screen.remove_widget(ListeningSessionScreen.host_bar)
            ListeningSessionScreen.host_bar = None
            self.screen_manager.ls_screen.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
        self.screen_manager.ls_screen.remove_widget(HostBar.drop_down)
        HostBar.drop_down = None
        HostBar.on_open = False

