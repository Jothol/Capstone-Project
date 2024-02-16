import kivy
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle, Color
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')

import src.database.account as account


class CreateAccount(Screen):
    username = "failed"
    password = "failed"

    def submit(self, username, password):
        account.create_account(username=username, password=password)
