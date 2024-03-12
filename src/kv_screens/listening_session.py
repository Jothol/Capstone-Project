import kivy
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')

from src.database import account
from src.database import session


class ListeningSessionScreen(Screen):

    def submit(self):
        sess = self.parent.ids.session_name
        user = self.parent.ids.username
        if sess.host.username == user.username:
            sess.remove_host()
        else:
            sess.remove_user(user)

        self.parent.ids.session_name = None
        self.manager.current = "session_home_page"

    def on_pre_enter(self, *args):
        sess = self.manager.ids.session_name
        self.ids.session_label.text = 'Welcome to {}!'.format(sess.name.id)
        self.ids.user_label.text = 'Hosted by: {}.'.format(sess.host.username)
        pass
