import kivy
from kivy.uix.screenmanager import Screen

from src.database import account
from src.database import session

kivy.require('2.3.0')


class ListeningSessionScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        sess = session.get_session("test_03")
        user = account.get_account("abc123")

    def on_enter(self):
        print(self.ids)
        print("Hello world")

    def on_leave(self, *args):
        sess = session.get_session("test_03")
        user = account.get_account("abc123")
        sess.remove_user(user)
