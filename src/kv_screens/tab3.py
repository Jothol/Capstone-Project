import os
import sys

import kivy
from kivy.app import App
from kivy.graphics import Color
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import src.database.account as account

kivy.require('2.3.0')


def build_dropdown_text(invites):
    print(invites)
    if invites == "":
        return 'Pending Invites (0)'
    else:
        return 'Pending Invites (' + str(len(invites.split(", "))) + ')'


def icon_button(button_type: str, invite: str, screen: Screen):
    source = ''
    if button_type == 'accept':
        source = '../other/images/accept_icon.png'
    elif button_type == 'decline':
        source = '../other/images/decline_icon.png'
    button = Button(size_hint=(None, None), size=(dp(30), dp(30)), background_color=(0, 0, 0, 0))
    icon = Image(source=source, center=button.center,
                 size=(0.6 * button.height, 0.6 * button.width))

    def update_icon_pos(instance, value):
        icon.center = button.center
    button.bind(pos=update_icon_pos, size=update_icon_pos)
    button.add_widget(icon)
    if button_type == 'accept':
        button.bind(on_press=lambda instance, inv=invite: screen.accept_invite(inv))
    elif button_type == 'decline':
        button.bind(on_press=lambda instance, inv=invite: screen.decline_invite(inv))
    return button


class Tab3(Screen):
    index = 3
    dropdown_open = False
    invites = ""
    friends = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        user = self.parent.parent.parent.parent.ids.username
        invites = self.invites = user.get_invites()
        self.ids.dropdown_box.children[0].text = build_dropdown_text(invites)
        friends = user.get_friends()
        friends_list = friends.split(", ")
        friends = "\n".join(friends_list)
        self.friends = friends
        self.ids.friend_list.text = "" + friends
        self.ids.account_info.text = ("Username: " + user.get_username() + "\nFirst Name: " + user.get_first_name() +
                                      "\nLast Name: " + user.get_last_name() + "\nEmail: " + user.get_email())

    def add_friend(self, username):
        if self.parent.parent.parent.parent.ids.username.add_friend(username):
            if self.friends != "":
                self.friends = self.friends + "\n"
            self.friends = self.friends + username
            self.ids.friend_list.text = "" + self.friends

    def invite_friend(self, username):
        self.parent.parent.parent.parent.ids.username.send_invite(username)

    def remove_friend(self, username):
        if self.parent.parent.parent.parent.ids.username.remove_friend(username):
            friends_list = self.friends.split("\n")
            friends_list.remove(username)
            self.friends = "\n".join(friends_list)
            self.ids.friend_list.text = "" + self.friends

    def toggle_dropdown(self):
        if self.dropdown_open:
            self.ids.dropdown_box.clear_widgets()
            button = Button(text=build_dropdown_text(self.invites), size_hint=(None, None), size=(dp(150), dp(50)))
            button.bind(on_press=lambda instance: self.toggle_dropdown())
            self.ids.dropdown_box.add_widget(button)
            self.dropdown_open = False
        else:
            if self.invites == "":
                return
            invites_list = self.invites.split(", ")
            for cnt, invite in enumerate(invites_list):
                entry = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(dp(150), dp(30)))
                username = Label(text=invite, size_hint=(None, None), size=(dp(90), dp(30)), color=(0, 0, 0, 1))
                accept = icon_button('accept', invite, self)
                decline = icon_button('decline', invite, self)
                entry.add_widget(username)
                entry.add_widget(accept)
                entry.add_widget(decline)
                self.ids.dropdown_box.add_widget(entry)
            self.dropdown_open = True

    def accept_invite(self, username):
        invites_list = self.invites.split(", ")
        invites_list.remove(username)
        self.invites = ", ".join(invites_list)
        self.toggle_dropdown()
        self.toggle_dropdown()
        if self.friends != "":
            self.friends = self.friends + "\n"
        self.friends = self.friends + username
        self.ids.friend_list.text = "" + self.friends
        self.parent.parent.parent.parent.ids.username.accept_invite(username)

    def decline_invite(self, username):
        self.parent.parent.parent.parent.ids.username.decline_invite(username)
        invites_list = self.invites.split(", ")
        invites_list.remove(username)
        self.invites = ", ".join(invites_list)
        self.toggle_dropdown()
        self.toggle_dropdown()

    def edit_account_info(self):
        print(self.parent.parent.parent.parent.current)

    def logout(self):
        App.get_running_app().logout()

    def delete_account(self):
        account.delete_account(App.get_running_app().screen_manager.ids.username.get_username())
        App.get_running_app().logout()
