import kivy
from kivy.uix.screenmanager import Screen, ScreenManager

import src.kv_screens.home
from src.database import account
from src.database import session

kivy.require('2.3.0')


class SessionHomeScreen(Screen):
    user = None
    session_name = None

    def submit(self, session_name, button_input):
        SessionHomeScreen.user = self.manager.ids.username
        # acc = account.get_account(SessionHomeScreen.user)
        if SessionHomeScreen.user.in_session is True:
            self.ids.error_message.text = "Already in a session"
            self.ids.error_message.color = [1, 0, 0, 1]
            return
        elif session_name == '':
            self.ids.error_message.text = "Cannot enter empty name"
            self.ids.error_message.color = [1, 0, 0, 1]
            return

        SessionHomeScreen.session_name = session.get_session(session_name)
        if SessionHomeScreen.session_name is None:
            if button_input == "Join":
                self.ids.error_message.text = "Session not found."
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                SessionHomeScreen.session_name = session.create_session(session_name, SessionHomeScreen.user)
                self.manager.ids.session_name = SessionHomeScreen.session_name
                self.ids.error_message.text = ''
                self.manager.current = "listening_session_page"
        else:
            if button_input == "Create":
                self.ids.error_message.text = "Session already created"
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                # SessionHomeScreen.session_name = session_name
                # sess = session.get_session(session_name)
                SessionHomeScreen.session_name.add_user(SessionHomeScreen.user)
                self.manager.ids.session_name = SessionHomeScreen.session_name
                self.ids.error_message.text = ''
                self.manager.current = "listening_session_page"
