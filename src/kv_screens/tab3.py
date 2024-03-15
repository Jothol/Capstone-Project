import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

kivy.require('2.3.0')


class Tab3(Screen):
    index = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Tab 3!"))

    def on_enter(self, *args):
        pass
