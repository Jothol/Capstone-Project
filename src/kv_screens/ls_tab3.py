import kivy
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager

from src.database import account

kivy.require('2.3.0')


class LS_Tab3(Screen):
    index = 3
    user = None
    session_name = None
    button_layout = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="LS_Tab 3!"))
        sm = ScreenManager()
        sm.ids.username = None
        sm.ids.session_name = None
        self.add_widget(sm)

    def on_enter(self, *args):
        pass

    def on_pre_enter(self, *args):
        LS_Tab3.user = self.manager.ids.username
        LS_Tab3.session_name = self.manager.ids.session_name
        if LS_Tab3.user.username == LS_Tab3.session_name.host.username:
            self.ids.add_button.background_color = [0, 1, 0, 1]
        else:
            self.ids.add_button.background_color = [1, 1, 1, 1]

    def open_add_account(self):
        sess = self.manager.ids.session_name
        user = self.manager.ids.username
        if sess.host.username != user.username:
            print("Only host can add users")
            return
        if LS_Tab3.button_layout is not None:
            self.remove_widget(LS_Tab3.button_layout)
            LS_Tab3.button_layout = None
            return

        bl = BoxLayout(orientation="vertical", size_hint=(.2, .2), size=(200, 200),
                       pos_hint={'center_x': .5, 'center_y': .5})
        bl.padding = 10
        bl.canvas.before.add(Color(1., 1., 1))
        bl.canvas.before.add(Rectangle(size=(300, 300), pos=(400, 200)))

        bl.add_widget(Label(text='Enter user to add', color=[0, 0.4, 0, 1]))
        bl.add_widget(TextInput(multiline=False, hint_text='User'))
        bl.add_widget(Button(text='Enter', background_color=[0, 1, 0, 1], size_hint=(.5, 1), pos_hint={'center_x': .5},
                             on_press=self.add_account))
        LS_Tab3.button_layout = bl
        print(LS_Tab3.button_layout)
        print(LS_Tab3.button_layout.children[0])

        self.add_widget(bl)

    @staticmethod
    def add_account(self):
        print("It works")
        user_name = LS_Tab3.button_layout.children[1].text
        user = account.get_account(user_name)
        if user is None:
            print("User not found")
        else:
            print("user found!")
            LS_Tab3.session_name.add_user(user)
        pass
