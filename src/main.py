import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from src.kv_screens.add_account_info import AddAccountInfo
from src.kv_screens.change_password import ChangePassword
from src.kv_screens.create_account import CreateAccount
from src.kv_screens.home import HomeScreen
from src.kv_screens.login import LoginScreen

import firebase_admin
from firebase_admin import credentials

from src.kv_screens.recommendation import RecommendationScreen
from src.kv_screens.recommendation_input import RecommendationInputScreen

from src.kv_screens.listening_session import ListeningSessionScreen


class Spotivibe(App):
    screen_manager = ScreenManager()

    def build(self):
        # Create the screen manager
        sm = self.screen_manager
        sm.ids.username = None
        sm.ids.recInput = ''
        sm.ids.session_name = None
        sm.add_widget(LoginScreen(name='login_page'))
        sm.add_widget(CreateAccount(name='create_account_page'))
        sm.add_widget(AddAccountInfo(name='add_account_info_page'))
        sm.add_widget(HomeScreen(name='home_page'))
        sm.add_widget(RecommendationScreen(name='recommendation_page'))
        sm.add_widget(RecommendationInputScreen(name='recommendation_input_page'))
        sm.add_widget(ListeningSessionScreen(name='listening_session_page'))
        sm.add_widget(ChangePassword(name='change_password_page'))

        Window.minimum_width = 800
        Window.minimum_height = 600

        return sm

    def check_user_session(self):
        if self.root.ids.session_name is not None:
            if self.root.ids.session_name.host.username == self.root.ids.username.username:
                self.root.ids.session_name.remove_host()
            else:
                self.root.ids.session_name.remove_user(self.root.ids.username)

    def logout(self):
        sm = self.screen_manager
        sm.ids.username = None
        sm.ids.recInput = ''
        sm.ids.session_name = None
        sm.clear_widgets()

        sm.add_widget(LoginScreen(name='login_page'))
        sm.add_widget(CreateAccount(name='create_account_page'))
        sm.add_widget(AddAccountInfo(name='add_account_info_page'))
        sm.add_widget(HomeScreen(name='home_page'))
        sm.add_widget(RecommendationScreen(name='recommendation_page'))
        sm.add_widget(RecommendationInputScreen(name='recommendation_input_page'))
        sm.add_widget(ListeningSessionScreen(name='listening_session_page'))
        sm.add_widget(ChangePassword(name='change_password_page'))


if __name__ == '__main__':
    cred = credentials.Certificate(r"..\other\database-access-key.json")
    firebase_admin.initialize_app(cred)

    Builder.load_file("kv_style/login.kv")
    Builder.load_file("kv_style/create_account.kv")
    Builder.load_file("kv_style/add_account_info.kv")
    Builder.load_file("kv_style/home.kv")
    Builder.load_file("kv_style/recommendation.kv")
    Builder.load_file("kv_style/recommendation_input.kv")
    Builder.load_file("kv_style/listening_session.kv")
    Builder.load_file("kv_style/tab1.kv")
    Builder.load_file("kv_style/tab2.kv")
    Builder.load_file("kv_style/tab3.kv")
    Builder.load_file("kv_style/ls_tab1.kv")
    Builder.load_file("kv_style/ls_tab2.kv")
    Builder.load_file("kv_style/ls_tab3.kv")

    # Spotivibe().run()

    sv = Spotivibe()
    sv.run()
    sv.check_user_session()
