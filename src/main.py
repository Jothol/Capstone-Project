from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from src.kv_screens.add_account_info import AddAccountInfo
from src.kv_screens.create_account import CreateAccount
from src.kv_screens.home import HomeScreen
from src.kv_screens.login import LoginScreen

import firebase_admin
from firebase_admin import credentials

from src.kv_screens.recommendation import RecommendationScreen
from src.kv_screens.recommendation_input import RecommendationInputScreen

from src.kv_screens.session_home import SessionHomeScreen
from src.kv_screens.listening_session import ListeningSessionScreen


class Spotivibe(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.ids.username = ''
        sm.ids.recInput = ''
        sm.add_widget(LoginScreen(name='login_page'))
        sm.add_widget(CreateAccount(name='create_account_page'))
        sm.add_widget(AddAccountInfo(name='add_account_info_page'))
        sm.add_widget(HomeScreen(name='home_page'))
        sm.add_widget(RecommendationScreen(name='recommendation_page'))
        sm.add_widget(RecommendationInputScreen(name='recommendation_input_page'))
        sm.add_widget(SessionHomeScreen(name='session_home_page'))
        sm.add_widget(ListeningSessionScreen(name='listening_session_page'))

        return sm


if __name__ == '__main__':
    cred = credentials.Certificate(r"..\other\database-access-key.json")
    firebase_admin.initialize_app(cred)

    Builder.load_file("kv_style/login.kv")
    Builder.load_file("kv_style/create_account.kv")
    Builder.load_file("kv_style/add_account_info.kv")
    Builder.load_file("kv_style/home.kv")
    Builder.load_file("kv_style/recommendation.kv")
    Builder.load_file("kv_style/recommendation_input.kv")
    Builder.load_file("kv_style/session_home.kv")
    Builder.load_file("kv_style/listening_session.kv")

    Spotivibe().run()
