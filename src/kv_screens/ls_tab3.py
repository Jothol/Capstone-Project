import kivy
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager

from src.database import account
from src.database import session

kivy.require('2.3.0')


class LS_Tab3(Screen):
    index = 3
    user = None
    session_name = None
    add_button_layout = None
    remove_button_layout = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="LS_Tab 3!"))
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        self.add_widget(sm)

    def on_pre_enter(self, *args):
        LS_Tab3.user = self.manager.ids.username
        LS_Tab3.session_name = self.manager.ids.session_name
        # if LS_Tab3.user.username == LS_Tab3.session_name.host.username:
        #     self.ids.add_button.background_color = [0, 1, 0, 1]
        #     self.ids.remove_button.background_color = [0, 1, 0, 1]
        # else:
        #     self.ids.add_button.background_color = [1, 1, 1, 1]
        #     self.ids.remove_button.background_color = [1, 1, 1, 1]

    # def open_add_account(self):
    #     sess = self.manager.ids.session_name
    #     user = self.manager.ids.username
    #     if sess.host.username != user.username:
    #         print("Only host can add users")
    #         return
    #     if LS_Tab3.add_button_layout is not None:
    #         self.remove_widget(LS_Tab3.add_button_layout)
    #         LS_Tab3.add_button_layout = None
    #         return
    #     if LS_Tab3.remove_button_layout is not None:
    #         self.remove_widget(LS_Tab3.remove_button_layout)
    #         LS_Tab3.remove_button_layout = None
    #
    #     bl = BoxLayout(orientation="vertical", size_hint=(.2, .2), size=(200, 200),
    #                    pos_hint={'center_x': .5, 'center_y': .5})
    #     bl.padding = 10
    #     bl.canvas.before.add(Color(1., 1., 1))
    #     bl.canvas.before.add(Rectangle(size=(800, 200), pos=(475, 300)))
    #
    #     bl.add_widget(Label(text='Enter user to add', color=[0, 0.4, 0, 1], bold=True))
    #     bl.add_widget(TextInput(multiline=False, hint_text='User'))
    #     bl.add_widget(Button(text='Enter', background_color=[0, 1, 0, 1], size_hint=(.5, 1), pos_hint={'center_x': .5},
    #                          ))
    #     LS_Tab3.add_button_layout = bl
    #
    #     self.add_widget(bl)

    # def open_remove_account(self):
    #     sess = self.manager.ids.session_name
    #     user = self.manager.ids.username
    #     if sess.host.username != user.username:
    #         print("Only host can add users")
    #         return
    #     if LS_Tab3.remove_button_layout is not None:
    #         self.remove_widget(LS_Tab3.remove_button_layout)
    #         LS_Tab3.remove_button_layout = None
    #         return
    #     if LS_Tab3.add_button_layout is not None:
    #         self.remove_widget(LS_Tab3.add_button_layout)
    #         LS_Tab3.add_button_layout = None
    #
    #     bl = BoxLayout(orientation="vertical", size_hint=(.2, .2), size=(200, 200),
    #                    pos_hint={'center_x': .5, 'center_y': .5})
    #     bl.padding = 10
    #     bl.canvas.before.add(Color(1., 1., 1))
    #     bl.canvas.before.add(Rectangle(size=(250, 200), pos=(475, 300)))
    #
    #     bl.add_widget(Label(text='Enter user to remove', color=[0, 0.4, 0, 1], bold=True))
    #     bl.add_widget(TextInput(multiline=False, hint_text='User'))
    #     bl.add_widget(Button(text='Enter', background_color=[0, 1, 0, 1], size_hint=(.5, 1), pos_hint={'center_x': .5},
    #                          on_press=self.remove_account))
    #     LS_Tab3.remove_button_layout = bl
    #
    #     self.add_widget(bl)

    # @staticmethod
    # def add_account(self):
    #     print("It works")
    #     user_name = LS_Tab3.add_button_layout.children[1].text
    #     user = account.get_account(user_name)
    #     if user is None:
    #         print("User not found")
    #     else:
    #         print("user found!")
    #         LS_Tab3.session_name.add_user(user)
    #     pass

    # @staticmethod
    # def remove_account(self):
    #     user_name = LS_Tab3.remove_button_layout[1].text
    #     user = account.get_account(user_name)
    #     if user is None:
    #         print("User not found")
    #     else:
    #         print("user found!")
    #         LS_Tab3.session_name.remove_user(user)
    #     pass

    def submit(self):
        sess = self.manager.ids.session_name
        user = self.manager.ids.username
        # Clock.unschedule(self.host_replacement)
        if sess.host.username == user.username:
            sess.remove_host()
            # self.remove_widget(LS_Tab3.host_bar)
            # cLS_Tab3.host_bar = None
        else:
            sess.remove_user(user)
