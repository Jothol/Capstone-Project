import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

kivy.require('2.3.0')


class Tab3(Screen):
    index = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # sm = ScreenManager()
        # sm.ids.username = ''
        # sm.ids.session_name = ''
        self.add_widget(Label(text="Tab 3!"))
        # self.add_widget(sm)

    def on_enter(self, *args):
        pass
