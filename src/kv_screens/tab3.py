import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')


class Tab3(Screen):
    index = 3
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Tab 3!"))

    def on_enter(self, *args):
        print(self)
        self.children[0].ids = self.manager.ids  # self.children[0] must be ScreenManager
        print(self.manager.ids)