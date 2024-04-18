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
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

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
    host_bar = None  # Used to show or hide the host_bar depending on the user
    screen_manager = None  # helper created for removing hostbar on ls_tab3
    user_list = None  # list of users pulled from firebase
    the_host_bar = None  # The creation of HostBar
    error_window_open = False  # Used for pop-up messages for Host Permissions

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

    def on_leave(self, *args):
        self.remove_widget(self.children[0])
        self.manager.ids.session_name = None
        bg_anim = Animation(padding=(0, 0, 0, 0))
        bg_anim.start(self.ids.background_image_container)
        Clock.unschedule(self.session_refresher)

    # Method process of User leaving session and back to home screen
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
                    ListeningSessionScreen.the_host_bar = HostBar(self, self.manager)
                    if self.manager.ids.session_name.session_status.get().get('status') == "public":
                        ListeningSessionScreen.the_host_bar.change_status()
                    ListeningSessionScreen.host_bar = ListeningSessionScreen.the_host_bar
                    self.add_widget(ListeningSessionScreen.host_bar)
                    self.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
            else:
                if ListeningSessionScreen.screen_manager.current == "ls_tab3":
                    self.remove_widget(ListeningSessionScreen.host_bar)
                    ListeningSessionScreen.host_bar = None

    # END OF CLOCK METHOD

    # BEGINNING OF POP-UP METHOD FOR HOST PERMISSIONS
    def animate_error_window(self, message: str, color):
        error_window = self.ids.error_window
        message_label = self.ids.window_message
        if message != '':
            message_label.text = message
            error_window.x = dp(-200)
        if error_window.x <= dp(-7):
            # self.ids.friend_input.text = ''
            self.error_window_open = True
            animation_window = Animation(pos=(error_window.x + dp(195), error_window.y), duration=0.1)
            error_window.opacity = 1
            message_label.color = color
            animation_window.start(error_window)
            Clock.schedule_once(lambda dt: self.animate_error_window('', (0, 0, 0, 0)), 5)
        else:
            self.error_window_open = False
            animation_window = Animation(pos=(error_window.x - dp(195), error_window.y), duration=0.1)
            animation_window.start(error_window)
            animation_window.bind(on_complete=lambda *args: setattr(error_window, 'opacity', 0))
            animation_window.bind(on_complete=lambda *args: setattr(message_label, 'text', ''))

    # END OF POP-UP METHOD FOR HOST PERMISSIONS


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
            bg_anim = Animation(padding=(dp(200), dp(200), dp(200), dp(200)), duration=0.35)
            bg_anim.start(self.parent.parent.ids.background_image_container)
            set_opacity(self.ids.settings_image, 0.5)
            Animation(size=(self.ids.setting_button.width * 0.7, self.ids.setting_button.height * 0.7),
                      center=self.ids.setting_button.center, duration=0.1).start(self.ids.settings_image)

        for i in self.screen_manager.screen_names:
            screen_to_switch = self.screen_manager.get_screen(i)
            if screen_to_switch.index == int(screen_name):
                break

        if self.screen_manager.current == 'ls_tab3' and int(screen_name) != 3:
            bg_anim = Animation(padding=(0, 0, 0, 0), duration=0.35)
            bg_anim.start(self.parent.parent.ids.background_image_container)
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

        # Including or Excluding HostBar
        if int(screen_name) == 3:
            if ListeningSessionScreen.host_bar is not None:
                self.screen_manager.ls_screen.remove_widget(ListeningSessionScreen.host_bar)
                ListeningSessionScreen.host_bar = None
                if HostBar.on_open is True:
                    self.screen_manager.ls_screen.remove_widget(HostBar.drop_down)
                    HostBar.on_open = False
                    HostBar.drop_down = None

        acc_username = self.screen_manager.ls_screen.user.username
        host_username = self.screen_manager.ls_screen.session_name.host.username
        if self.screen_manager.current_screen.name == "ls_tab3":
            if host_username == acc_username:
                # Next line is in order to make the buttons centered again (idk why the problem would exist)
                ListeningSessionScreen.the_host_bar = (
                    HostBar(self.screen_manager.ls_screen, self.screen_manager))
                if self.screen_manager.ids.session_name.session_status.get().get('status') == "public":
                    ListeningSessionScreen.the_host_bar.change_status()
                ListeningSessionScreen.host_bar = ListeningSessionScreen.the_host_bar
                self.screen_manager.ls_screen.add_widget(ListeningSessionScreen.host_bar)

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_to_switch.name


class HostBar(BoxLayout):
    on_open = False
    drop_down = None
    input_text = ""
    status = "Private"

    def __init__(self, ls_screen: ListeningSessionScreen, screen_manager: ScreenManager, **kwargs):
        super(HostBar, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.screen_manager.ids = ls_screen.parent.ids
        self.screen_manager.ls_screen = ls_screen

    def change_status(self):
        if self.ids.status.text == "Private":
            self.ids.status.text = "Public"
            HostBar.status = "Public"
            self.ids.status.background_color = [0, 1, 0.6, 1]
            self.screen_manager.ids.session_name.session_status.update({'status': 'public'})
        else:
            self.ids.status.text = "Private"
            HostBar.status = "Private"
            self.ids.status.background_color = [1, 0, 0.4, 1]
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

    def end_session(self):
        dark = DarkenScreen2(self.screen_manager.ls_screen)
        self.screen_manager.ls_screen.add_widget(dark)


class HostDropBar(BoxLayout):
    def __init__(self, ls_screen: ListeningSessionScreen, screen_manager: ScreenManager, **kwargs):
        super(HostDropBar, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.screen_manager.ids = ls_screen.parent.ids
        self.screen_manager.ls_screen = ls_screen

    def submit(self, user_name):
        if user_name == "":
            self.screen_manager.ls_screen.animate_error_window('Must enter valid name.', (1, 0, 0, 1))
            self.screen_manager.ls_screen.remove_widget(HostBar.drop_down)
            HostBar.drop_down = None
            HostBar.on_open = False
            return

        user = account.get_account(user_name)
        sess = ListeningSessionScreen.session_name
        if self.ids.input_label.text == "Enter invited user:":
            # Check for a case where user is already in session
            if user is None:
                self.screen_manager.ls_screen.animate_error_window('User not found.', (1, 0, 0, 1))
            elif session.get_user(sess.name, user_name) is not None:
                self.screen_manager.ls_screen.animate_error_window('User is already in session.',
                                                                   (1, 0, 0, 1))
            else:
                try:
                    index = user.friends.index(sess.host.username)
                    if sess.name.id in user.session_invites:
                        self.screen_manager.ls_screen.animate_error_window('User already received invite.',
                                                                           (1, 0, 0, 1))
                    else:
                        user.session_invites.append(sess.name.id)
                        user.account.update({'session_invites': user.session_invites})
                        self.screen_manager.ls_screen.animate_error_window('Invite to ' + user_name + ' sent.',
                                                                           (0, 0.5, 0, 1))
                except ValueError:
                    self.screen_manager.ls_screen.animate_error_window('You are not friends with the user.',
                                                                       (1, 0, 0, 1))
        elif self.ids.input_label.text == "Enter removed user:":
            if session.get_user(sess.name, user_name) is None:
                self.screen_manager.ls_screen.animate_error_window('User not found in session.', (1, 0, 0, 1))
            else:
                sess.remove_user(user)
                self.screen_manager.ls_screen.animate_error_window('User ' + user_name + 'removed.', (0, 0.5, 0, 1))
        elif self.ids.input_label.text == "Enter new host:":
            if session.get_user(sess.name, user_name) is None:
                self.screen_manager.ls_screen.animate_error_window('User not found in session.', (1, 0, 0, 1))
                self.screen_manager.ls_screen.remove_widget(HostBar.drop_down)
                HostBar.drop_down = None
                HostBar.on_open = False
                return
            sess.name.update({ListeningSessionScreen.user.username: 'user'})
            sess.name.update({user_name: 'host'})
            sess.host = user
            self.screen_manager.ls_screen.animate_error_window(user_name + ' is the new host.', (0, 0.5, 0, 1))
            self.screen_manager.ls_screen.remove_widget(ListeningSessionScreen.host_bar)
            ListeningSessionScreen.host_bar = None
            self.screen_manager.ls_screen.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
        self.screen_manager.ls_screen.remove_widget(HostBar.drop_down)
        HostBar.drop_down = None
        HostBar.on_open = False


class DarkenScreen2(FloatLayout):

    def __init__(self, ls_screen: ListeningSessionScreen, **kwargs):
        super().__init__(**kwargs)
        self.dark_rectangle = Rectangle()
        self.darken()
        self.box = are_you_sure = create_boxlayout()
        are_you_sure.add_widget(Label(text="End Session", font_size=dp(20), color=(0, 0, 0, 1), bold=True,
                                      size_hint=(None, None), size=(dp(180), dp(30))))
        are_you_sure.add_widget(Label(text="\n*Are you sure you want to end", color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(23)), font_size=dp(11)))
        are_you_sure.add_widget(Label(text="the session? Everyone else will be", color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(12)), font_size=dp(11)))
        are_you_sure.add_widget(Label(text="removed from the session.", color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(12)), font_size=dp(11)))
        are_you_sure.add_widget(BoxLayout(orientation="horizontal"))
        options = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint=(None, None), size=(dp(180), dp(30)))
        yes = Button(text="Delete")
        yes.bind(on_release=lambda instance: self.delete_session())
        no = Button(text="Cancel", background_color=(0, 1, 0, 1))
        no.bind(on_release=lambda instance: self.cancel())
        options.add_widget(yes)
        options.add_widget(no)
        are_you_sure.add_widget(options)
        self.add_widget(are_you_sure)
        self.ls = ls_screen
        print("Itch", self.ls)

    def delete_session(self):
        self.ls.parent.ids.session_name = None
        self.ls.manager.current = "home_page"
        for col in ListeningSessionScreen.session_name.name.collections():
            for doc in col.list_documents():
                doc.delete()
        user_list = ListeningSessionScreen.session_name.name.get().to_dict()
        while user_list.__len__() > 0:
            temp = user_list.popitem()
            acc = account.get_account(temp[0])
            acc.account.update({'in_session': False})
            acc.in_session = False

        self.ls.parent.ids.username.in_session = False
        ListeningSessionScreen.session_name.name.delete()  # actual deletion of session name in firebase
        self.ls.remove_widget(self)
        self.ls.remove_widget(ListeningSessionScreen.host_bar)
        ListeningSessionScreen.host_bar = None

    def cancel(self):
        self.parent.remove_widget(self)

    def darken(self):
        with self.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black color
            self.dark_rectangle = Rectangle(pos=self.pos, size=Window.size)

    def on_size(self, *args):
        self.dark_rectangle.size = args[1]

    def on_pos(self, *args):
        self.dark_rectangle.pos = args[1]

    def on_touch_down(self, touch):
        if self.box.children[0].collide_point(*touch.pos):
            return super().on_touch_down(touch)
        else:
            return True

    def on_touch_move(self, touch):
        return True

    def on_touch_up(self, touch):
        return True


def create_boxlayout():
    box_layout = BoxLayout(
        orientation='vertical',
        size_hint=(None, None),
        size=(dp(200), dp(150)),
        pos_hint={'center_x': 0.5, 'center_y': 0.5},
        padding=dp(10)
    )

    with box_layout.canvas.before:
        Color(1, 1, 1, 1)  # White color
        box_layout.rounded_rectangle = RoundedRectangle(pos=box_layout.pos, size=box_layout.size, radius=[10])

    box_layout.bind(size=lambda instance, value: setattr(box_layout.rounded_rectangle, 'size', value))
    box_layout.bind(pos=lambda instance, value: setattr(box_layout.rounded_rectangle, 'pos', value))

    return box_layout
