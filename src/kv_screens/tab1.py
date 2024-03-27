import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from src.kv_screens.session_home import SessionHomeScreen
from src.kv_screens.listening_session import ListeningSessionScreen
from src.kv_screens import player

kivy.require('2.3.0')

sp = player.sp


class Tab1(Screen):
    index = 1
    device_dropdown = ObjectProperty(None)

    # self is tab1 screen
    # self.manager is ScreenManager for tab1 screen
    # self.manager.parent is boxlayout child from home
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sm = ScreenManager()
        sm.ids.username = ''
        sm.ids.session_name = ''
        sm.add_widget(SessionHomeScreen(name='session_home_page'))
        sm.add_widget(ListeningSessionScreen(name='listening_session_page'))
        self.add_widget(sm)
        self.device_dropdown = DropDown()
        self.create_device_dropdown()
        self.dropdown_button = Button(text='Devices', size_hint=(None, None), size=(110, 50))
        self.dropdown_button.bind(on_release=self.open_dropdown)

        self.add_widget(self.dropdown_button)

    def on_enter(self, *args):
        # self has multiple files gathered in arrays, so get only one child
        # make sure you are getting the ScreenManager for session_home and listening_session
        # self.children[0] is currently the ScreenManager for them
        print(self.children)
        self.children[1].ids.username = self.manager.ids.username
        self.manager.ids.session_name = self.children[1].ids.session_name

        pass

    def open_dropdown(self, instance):
        self.create_device_dropdown()
        self.device_dropdown.open(instance)

    def select_option(self, button):
        print(f'Selected option: {button}')
        player.set_device_id(button.id)

    def create_device_dropdown(self):
        print("Creating device dropdown.")
        # get rid of any buttons created before this call
        self.device_dropdown.clear_widgets()
        devices = player.get_devices(sp)
        if devices is None:
            print("Devices is None.")
            warning = Label(text="No devices found!", size_hint_y=None, height=44)
            self.device_dropdown.add_widget(warning)
        else:
            for device in devices['devices']:
                button = Button(text=f'{device['name']}', size_hint_y=None, height=44)
                button.id = device['id']
                button.bind(on_release=self.select_option)
                self.device_dropdown.add_widget(button)
