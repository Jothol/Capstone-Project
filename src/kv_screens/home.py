import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

from src.database import account
from src.database.account import Account
from src.kv_screens.tab1 import Tab1
from src.kv_screens.tab2 import Tab2
from src.kv_screens.tab3 import Tab3

kivy.require('2.3.0')


class HomeScreen(Screen):
    username = ''
    session_name = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.parent)
        bl = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        sm.add_widget(Tab1(name='tab1'))
        sm.add_widget(Tab2(name='tab2'))
        sm.add_widget(Tab3(name='tab3'))
        bl.add_widget(sm)
        bl.add_widget(TabBar(sm))
        self.add_widget(bl)


class TabBar(FloatLayout):

    def __init__(self, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager

    def switch_screen(self, screen_name):
        # Access the ScreenManager and switch to the desired screen
        screen_to_switch = self.screen_manager.get_screen(screen_name)

        # Determine the direction of the transition
        if screen_to_switch.index > self.screen_manager.current_screen.index:
            direction = 'left'
        else:
            direction = 'right'

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_name
