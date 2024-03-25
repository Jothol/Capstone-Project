import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from src.database import session

from src.kv_screens.listening_session import ListeningSessionScreen

kivy.require('2.3.0')


class Tab1(Screen):
    index = 1
    user = None
    session_name = None

    # self is tab1 screen
    # self.manager is ScreenManager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        self.add_widget(sm)

    def on_enter(self, *args):
        # self has multiple files gathered in arrays, so get only one child
        # make sure you are getting the ScreenManager for session_home and listening_session
        # self.children[0] is currently the ScreenManager for them
        self.children[0].ids.username = self.manager.ids.username
        self.manager.ids.session_name = self.children[0].ids.session_name

        pass

    def on_leave(self, *args):
        pass

    def open_dropdown(self, instance):
        dropdown = self.ids.dropdown
        dropdown.open(instance)

    def select_option(self, option):
        print(f'Selected option: {option}')

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
                self.ids.error_message.text = "Session not found."
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                Tab1.session_name = session.create_session(session_name, Tab1.user)
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name
                self.ids.error_message.text = ''
                print(self.manager.home_screen.manager.current)
                self.manager.home_screen.manager.current = "listening_session_page"
        else:
            if button_input == "Create":
                self.ids.error_message.text = "Session already created"
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                # SessionHomeScreen.session_name = session_name
                # sess = session.get_session(session_name)
                Tab1.session_name.add_user(Tab1.user)
                self.manager.home_screen.manager.ids.session_name = Tab1.session_name
                self.ids.error_message.text = ''
                self.manager.home_screen.manager.current = "listening_session_page"

        pass
