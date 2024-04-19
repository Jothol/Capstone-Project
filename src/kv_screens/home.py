import sys

import kivy
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

from src.database import account, socket_client
from src.database.account import Account
from src.kv_screens.chat import ChatScreen
from src.kv_screens.tab1 import Tab1
from src.kv_screens.tab2 import Tab2
from src.kv_screens.tab3 import Tab3

kivy.require('2.3.0')


def show_error(message):
    print(message)
    Clock.schedule_once(sys.exit, 10)


def set_opacity(image: Image, opacity):
    # Find the Color instruction in canvas.after
    for instruction in image.canvas.after.children:
        if isinstance(instruction, Color):
            # Modify the opacity value
            instruction.rgba = (instruction.rgba[0], instruction.rgba[1], instruction.rgba[2], opacity)
            break


class HomeScreen(Screen):
    chat_screen_exists = False
    accessed = False

    # self is home screen
    # self.parent is main.py
    def on_enter(self):
        if not self.accessed:
            bl = BoxLayout(orientation='vertical')
            sm = ScreenManager()
            sm.ids = self.parent.ids
            sm.add_widget(Tab1(name='tab1'))
            sm.add_widget(Tab2(name='tab2'))
            sm.add_widget(Tab3(name='tab3'))
            bl.ids = self.parent.ids
            bl.add_widget(sm)
            bl.add_widget(TabBar(self, sm))

            self.add_widget(bl)
            self.accessed = True

    def switch_to(self):
        pass


class TabBar(FloatLayout):

    # self is TabBar object
    # self.screen_manager is ScreenManager for TabBar
    # self.parent is BoxLayout object (child of home screen)
    def __init__(self, home_screen: HomeScreen, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager
        self.screen_manager.ids = home_screen.manager.ids
        self.screen_manager.home_screen = home_screen

    def switch_screen(self, screen_name):
        screen_to_switch = ''

        set_opacity(self.ids.home_image, 0)
        # set_opacity(self.ids.search_image, 0)
        set_opacity(self.ids.settings_image, 0)

        if int(screen_name) == 1:
            set_opacity(self.ids.home_image, 0.5)
            Animation(size=(self.ids.home_button.width * 0.8, self.ids.home_button.height * 0.8),
                      center=self.ids.home_button.center, duration=0.1).start(self.ids.home_image)
        elif int(screen_name) == 2:
            set_opacity(self.ids.search_image, 0.5)
            Animation(size=(self.ids.search_button.width * 0.7, self.ids.search_button.height * 0.7),
                      center=self.ids.search_button.center, duration=0.1).start(self.ids.search_image)
        else:
            bg_anim = Animation(padding=(dp(200), dp(200), dp(200), dp(200)), duration=0.35)
            bg_anim.start(self.parent.parent.ids.background_image_container)
            set_opacity(self.ids.settings_image, 0.5)
            Animation(size=(self.ids.setting_button.width * 0.7, self.ids.setting_button.height * 0.7),
                      center=self.ids.setting_button.center, duration=0.1).start(self.ids.settings_image)

        for i in self.screen_manager.screen_names:
            screen_to_switch = self.screen_manager.get_screen(i)
            if screen_to_switch.index == int(screen_name):
                break

        if self.screen_manager.current == 'tab3' and int(screen_name) != 3:
            bg_anim = Animation(padding=(0, 0, 0, 0), duration=0.35)
            bg_anim.start(self.parent.parent.ids.background_image_container)
            Animation(size=(self.ids.setting_button.width * 0.5, self.ids.setting_button.height * 0.5),
                      center=self.ids.setting_button.center, duration=0.1).start(self.ids.settings_image)
        elif self.screen_manager.current == 'tab2' and int(screen_name) != 2:
            Animation(size=(self.ids.search_button.width * 0.5, self.ids.search_button.height * 0.5),
                      center=self.ids.search_button.center, duration=0.1).start(self.ids.search_image)
        elif self.screen_manager.current == 'tab1' and int(screen_name) != 1:
            Animation(size=(self.ids.home_button.width * 0.6, self.ids.home_button.height * 0.6),
                      center=self.ids.home_button.center, duration=0.1).start(self.ids.home_image)

        self.screen_manager.ids = self.screen_manager.parent.ids

        # Determine the direction of the transition
        if screen_to_switch.index > self.screen_manager.current_screen.index:
            direction = 'left'
        else:
            direction = 'right'

        # Set the transition and switch to the desired screen
        self.screen_manager.transition = SlideTransition(direction=direction)
        self.screen_manager.current = screen_to_switch.name
