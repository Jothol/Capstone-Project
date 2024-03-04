import kivy
from kivy.uix.screenmanager import Screen

from src.database import account
from src.database import session

kivy.require('2.3.0')


class SessionHomeScreen(Screen):
    def submit(self, session_name):
        if session.get_session(session_name) is None:
            self.ids.error_message.text = "Session not found."
            self.ids.error_message.color = [1, 0, 0, 1]
        else:
            self.parent.ids.session_name = session_name
            sess = session.get_session(session_name)
            user = account.get_account('abc123')
            sess.add_user(user)
            self.parent.current = "listening_session_page"
