import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')


class Tab2(Screen):
    index = 2
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Tab 2!"))
