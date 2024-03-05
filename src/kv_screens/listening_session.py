import kivy
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')

from src.database import account
from src.database import session


class ListeningSessionScreen(Screen):

    def submit(self):
        sess = session.get_session(self.parent.ids.session_name)
        user = account.get_account(self.parent.ids.username)
        if sess.host.username == user.username:
            sess.remove_host()
        else:
            sess.remove_user(user)

        self.parent.ids.session_name = ''
