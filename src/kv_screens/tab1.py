import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty

from src.database import session

from src.kv_screens.listening_session import ListeningSessionScreen
from src.kv_screens import player
from src.kv_screens.hoverablebutton import HoverableButton

kivy.require('2.3.0')

sp = player.sp


class Tab1(Screen):
    index = 1
    device_dropdown = ObjectProperty(None)
    invite_dropdown = ObjectProperty(None)
    user = None
    session_name = None


    # self is tab1 screen
    # self.manager is ScreenManager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invite_button = None
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        self.add_widget(sm)
        self.device_dropdown = DropDown()
        self.create_device_dropdown()
        self.dropdown_button = HoverableButton(text='Devices', size_hint=(None, None), size=(110, 50), offset=(0, -50),
                                               transition_color="grey")
        self.dropdown_button.bind(on_release=self.open_dropdown)

        self.add_widget(self.dropdown_button)

    def on_enter(self, *args):
        # self has multiple files gathered in arrays, so get only one child
        # make sure you are getting the ScreenManager for session_home and listening_session
        # self.children[0] is currently the ScreenManager for them
        print(self.children)
        self.children[1].ids.username = self.manager.ids.username
        self.manager.ids.session_name = None
        self.ids.welcome_label.text = 'Welcome, {}!'.format(self.manager.ids.username.username)

        if len(self.manager.ids.username.session_invites) != 0:
            self.invite_dropdown = DropDown()
            for invite in self.manager.ids.username.session_invites:
                button = Button(text=invite, size_hint_y=None, height=44, pos=(800, 10))
                # button.bind(on_release=self.select_option)
                self.invite_dropdown.add_widget(button)

            self.add_widget(self.invite_dropdown)
            self.invite_button = Button(text='Invites', size_hint=(None, None), size=(180, 50), pos=(800, 10))
            self.invite_button.bind(on_release=self.open_invites)
            self.add_widget(self.invite_button)

        pass

    def on_leave(self, *args):
        pass

    def open_dropdown(self, instance):
        self.create_device_dropdown()
        self.device_dropdown.open(instance)

    def open_invites(self, instance):
        pass

    def select_option(self, button):
        print(f'Selected option: {button}')
        player.set_device_id(button.id)

    def create_device_dropdown(self):
        print("Creating device dropdown.")
        # get rid of any buttons created before this call
        self.device_dropdown.clear_widgets()
        devices = player.get_devices(sp)
        if devices is None:
            print("Devices is None.")
            warning = Label(text="No devices found!", size_hint_y=None, height=44)
            self.device_dropdown.add_widget(warning)
        else:
            for device in devices['devices']:
                button = Button(text=f'{device['name']}', size_hint_y=None, height=44)
                button.id = device['id']
                button.bind(on_release=self.select_option)
                self.device_dropdown.add_widget(button)

    def submit(self, session_name, button_input):
        Tab1.user = self.manager.ids.username
        if Tab1.user.in_session is True:
            self.ids.error_message.text = "Already in a session"
            self.ids.error_message.color = [1, 0, 0, 1]
            return
        elif session_name == '':
            self.ids.error_message.text = "Cannot enter empty name"
            self.ids.error_message.color = [1, 0, 0, 1]
            return

        Tab1.session_name = session.get_session(session_name)
        if Tab1.session_name is None:
            if button_input == "Join":
                self.ids.error_message.color = [1, 0, 0, 1]
                try:
                    print("Hello 1")
                    Tab1.user.session_invites = Tab1.user.account.get().get('session_invites')
                    index = Tab1.user.session_invites.index(session_name)
                    Tab1.user.session_invites.pop(index)
                    Tab1.user.account.update({'session_invites': Tab1.user.session_invites})
                    self.ids.error_message.text = "Session ended."
                except ValueError:
                    self.ids.error_message.text = "Session not found."
                    return
            else:
                Tab1.session_name = session.create_session(session_name, Tab1.user)
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name
                self.ids.error_message.text = ''
                self.manager.home_screen.manager.current = "listening_session_page"
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name
        else:
            if button_input == "Create":
                self.ids.error_message.text = "Session already created"
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                try:
                    Tab1.user.session_invites = Tab1.user.account.get().get('session_invites')
                    index = Tab1.user.session_invites.index(Tab1.session_name.name.id)
                    Tab1.user.session_invites.pop(index)
                    Tab1.user.account.update({'session_invites': Tab1.user.session_invites})
                except ValueError:
                    self.ids.error_message.text = "User not invited."
                    return

                # SessionHomeScreen.session_name = session_name
                # sess = session.get_session(session_name)
                Tab1.session_name.add_user(Tab1.user)
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name
                self.ids.error_message.text = ''
                self.manager.home_screen.manager.current = "listening_session_page"
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name

        pass
