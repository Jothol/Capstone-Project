import kivy
from kivy.uix.screenmanager import Screen

from src.database import account
from src.database import session

kivy.require('2.3.0')


class SessionHomeScreen(Screen):
    user = ''

    def submit(self, session_name, button_input):
        print(self.parent.parent.ids)
        SessionHomeScreen.user = self.parent.ids.username
        acc = account.get_account(SessionHomeScreen.user)
        if acc.in_session is True:
            self.ids.error_message.text = "Already in a session"
            self.ids.error_message.color = [1, 0, 0, 1]
            return
        elif session_name is '':
            self.ids.error_message.text = "Cannot enter empty name"
            self.ids.error_message.color = [1, 0, 0, 1]
            return
        elif session.get_session(session_name) is None:
            if button_input is "Join":
                self.ids.error_message.text = "Session not found."
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                self.parent.ids.session_name = session_name
                session.create_session(session_name, SessionHomeScreen.user)
                self.parent.current = "listening_session_page"
        else:
            if button_input is "Create":
                self.ids.error_message.text = "Session already created"
                self.ids.error_message.color = [1, 0, 0, 1]
            else:
                self.parent.ids.session_name = session_name
                sess = session.get_session(session_name)
                sess.add_user(account.get_account(SessionHomeScreen.user))
                self.parent.current = "listening_session_page"
