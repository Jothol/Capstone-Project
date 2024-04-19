import kivy
from kivy.graphics import Color, Line, BorderImage, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

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
    create_session_friends = []

    # self is tab1 screen
    # self.manager is ScreenManager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        self.add_widget(sm)
        self.device_dropdown = DropDown()
        self.create_device_dropdown()
        self.dropdown_button = HoverableButton(text='Devices', size_hint=(None, None), size=(110, 50), offset=(0, -50),
                                               transition_color="grey")
        self.dropdown_button.bind(on_release=self.open_dropdown)
        self.dropdown_button.opacity = 0

        self.add_widget(self.dropdown_button)

    def on_enter(self, *args):
        # self has multiple files gathered in arrays, so get only one child
        # make sure you are getting the ScreenManager for session_home and listening_session
        # self.children[0] is currently the ScreenManager for them
        self.children[1].ids.username = self.manager.ids.username
        self.manager.ids.session_name = None
        self.ids.welcome_label.text = 'Welcome, {}!'.format(self.manager.ids.username.username)
        self.create_session_friends = []

    def open_dropdown(self, instance):
        self.create_device_dropdown()
        self.device_dropdown.open(instance)

    def button_submit(self, instance):
        self.submit(instance.text, "Join")

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
        else:
            if button_input == "Create":
                self.ids.error_message.text = "Session already created"
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                if Tab1.session_name.session_status.get().get("status") == "private":
                    try:
                        Tab1.user.session_invites = Tab1.user.account.get().get('session_invites')
                        index = Tab1.user.session_invites.index(Tab1.session_name.name.id)
                        Tab1.user.session_invites.pop(index)
                        Tab1.user.account.update({'session_invites': Tab1.user.session_invites})
                    except ValueError:
                        self.ids.error_message.text = "User not invited."
                        self.ids.error_message.color = [1, 0, 0, 1]
                        return

                # SessionHomeScreen.session_name = session_name
                # sess = session.get_session(session_name)
                Tab1.session_name.add_user(Tab1.user)
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name
                self.manager.home_screen.manager.ids.username = Tab1.user
                self.ids.error_message.text = ''
                self.manager.home_screen.manager.current = "listening_session_page"
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name

        ListeningSessionScreen.auto_friends_list = self.create_session_friends

    def create_session(self, is_closed):
        if not is_closed:
            self.ids.scroll_contents.clear_widgets()
            self.create_session_friends = []
            self.ids.create_session_window.pos_hint = {'center_x': -0.5}
            self.ids.create_session.disabled = False
            self.ids.join_session.disabled = False
            return
        friends = self.manager.home_screen.manager.ids.username.get_friends().split(', ')
        for friend in friends:
            scroll = self.ids.scroll_contents
            option = Option()
            option.set_text(friend)
            scroll.add_widget(option)
        self.ids.create_session_window.pos_hint = {'center_x': 0.5}
        self.ids.create_session.disabled = True
        self.ids.join_session.disabled = True

    def join_session(self, is_closed):
        if not is_closed:
            self.ids.join_session_window.pos_hint = {'center_x': -0.5}
            self.ids.create_session.disabled = False
            self.ids.join_session.disabled = False
            return
        self.manager.ids.username.session_invites = self.manager.ids.username.account.get().get('session_invites')
        print(self.manager.ids.username.session_invites)
        for invite in self.manager.ids.username.session_invites:
            scroll = self.ids.scroll_contents_2
            option = Option2()
            option.set_text(invite)
            scroll.add_widget(option)
        self.ids.join_session_window.pos_hint = {'center_x': 0.5}
        self.ids.create_session.disabled = True
        self.ids.join_session.disabled = True


class Option(BoxLayout):

    def __init__(self):
        super(Option, self).__init__()

    def set_text(self, text):
        self.ids.option_label.text = text

    def add(self, username):
        tab1 = self.parent.parent.parent.parent.parent
        tab1.create_session_friends.append(username)
        self.remove_widget(self.children[0])
        self.add_widget(RemoveButton())
        self.ids.option_label.opacity = 1
        self.ids.option_label.font_size = self.ids.option_label.font_size + dp(1)

    def remove(self, username):
        tab1 = self.parent.parent.parent.parent.parent
        tab1.create_session_friends.remove(username)
        self.remove_widget(self.children[0])
        self.add_widget(AddButton())
        self.ids.option_label.opacity = 0.4
        self.ids.option_label.font_size = self.ids.option_label.font_size - dp(1)


class AddButton(Button):
    def __init__(self, **kwargs):
        super(AddButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(25), dp(25))
        self.pos_hint = {'center_y': 0.5}
        self.background_color = (0, 0, 0, 0)
        self.bind(on_release=self.on_press)

        icon = Image(source='../other/images/accept_icon.png', center=self.center,
                     size=(0.6 * self.height, 0.6 * self.width))

        self.bind(pos=lambda instance, value: setattr(icon, 'center', instance.center))
        self.bind(size=lambda instance, value: setattr(icon, 'center', instance.center))
        self.add_widget(icon)

    def on_press(self, *args):
        self.parent.add(self.parent.ids.option_label.text)


class RemoveButton(Button):
    def __init__(self, **kwargs):
        super(RemoveButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(25), dp(25))
        self.pos_hint = {'center_y': 0.5}
        self.background_color = (0, 0, 0, 0)
        self.bind(on_release=self.on_press)

        icon = Image(source='../other/images/decline_icon.png', center=self.center,
                     size=(0.6 * self.height, 0.6 * self.width))

        self.bind(pos=lambda instance, value: setattr(icon, 'center', instance.center))
        self.bind(size=lambda instance, value: setattr(icon, 'center', instance.center))
        self.add_widget(icon)

    def on_press(self, *args):
        self.parent.remove(self.parent.ids.option_label.text)


class Option2(BoxLayout):
    def __init__(self, **kwargs):
        super(Option2, self).__init__(**kwargs)

    def set_text(self, text):
        self.ids.option_label_2.text = text

    def join_session(self):
        self.remove_widget(self.children[0])
        self.add_widget(YesButton())
        self.add_widget(NoButton())
        self.ids.option_label_2.opacity = 1
        self.ids.option_label_2.font_size = self.ids.option_label_2.font_size + dp(1)

    def yes(self, code):
        self.parent.parent.parent.parent.parent.submit(code, "Join")

    def no(self):
        self.remove_widget(self.children[0])
        self.remove_widget(self.children[0])
        self.add_widget(JoinButton())
        self.ids.option_label_2.opacity = 0.4
        self.ids.option_label_2.font_size = self.ids.option_label_2.font_size - dp(1)


class YesButton(Button):
    def __init__(self, **kwargs):
        super(YesButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(25), dp(25))
        self.pos_hint = {'center_y': 0.5}
        self.background_color = (0, 0, 0, 0)
        self.bind(on_release=self.on_press)

        icon = Image(source='../other/images/join_icon.png', center=self.center,
                     size=(0.55 * self.height, 0.55 * self.width))

        self.bind(pos=lambda instance, value: setattr(icon, 'center', instance.center))
        self.bind(size=lambda instance, value: setattr(icon, 'center', instance.center))
        self.add_widget(icon)

    def on_press(self, *args):
        self.parent.yes(self.parent.ids.option_label_2.text)


class NoButton(Button):
    def __init__(self, **kwargs):
        super(NoButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(25), dp(25))
        self.pos_hint = {'center_y': 0.5}
        self.background_color = (0, 0, 0, 0)
        self.bind(on_release=self.on_press)

        icon = Image(source='../other/images/decline_icon.png', center=self.center,
                     size=(0.6 * self.height, 0.6 * self.width))

        self.bind(pos=lambda instance, value: setattr(icon, 'center', instance.center))
        self.bind(size=lambda instance, value: setattr(icon, 'center', instance.center))
        self.add_widget(icon)

    def on_press(self, *args):
        self.parent.no()


class JoinButton(Button):
    def __init__(self, **kwargs):
        super(JoinButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(50), dp(20))
        self.font_size = dp(12)
        self.text = 'Join'
        self.pos_hint = {'center_y': 0.5}
        self.background_color = (0, 1, 0, 1)
        self.bind(on_release=self.on_press)

    def on_press(self, *args):
        self.parent.join_session()
