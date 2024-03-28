import kivy
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
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


class Tab3(Screen):
    index = 3
    dropdown_open = False
    invites = ""
    friends = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        invites = self.invites = self.parent.parent.parent.parent.ids.username.get_invites()
        self.ids.dropdown_box.children[0].text = build_dropdown_text(invites)
        friends = self.parent.parent.parent.parent.ids.username.get_friends()
        friends_list = friends.split(", ")
        friends = "\n".join(friends_list)
        self.friends = friends
        self.ids.friend_list.text = "Friends:\n" + friends

    def add_friend(self, username):
        if self.parent.parent.parent.parent.ids.username.add_friend(username):
            if self.friends != "":
                self.friends = self.friends + "\n"
            self.friends = self.friends + username
            self.ids.friend_list.text = "Friends:\n" + self.friends

    def invite_friend(self, username):
        self.parent.parent.parent.parent.ids.username.send_invite(username)

    def remove_friend(self, username):
        if self.parent.parent.parent.parent.ids.username.remove_friend(username):
            friends_list = self.friends.split("\n")
            friends_list.remove(username)
            self.friends = "\n".join(friends_list)
            self.ids.friend_list.text = "Friends:\n" + self.friends

    def toggle_dropdown(self):
        if self.dropdown_open:
            self.ids.dropdown_box.clear_widgets()
            button = Button(text=build_dropdown_text(self.invites), size_hint=(None, None), size=(dp(170), dp(50)))
            button.bind(on_press=lambda instance: self.toggle_dropdown())
            self.ids.dropdown_box.add_widget(button)
            self.dropdown_open = False
        else:
            if self.invites == "":
                return
            invites_list = self.invites.split(", ")
            for cnt, invite in enumerate(invites_list):
                entry = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(dp(120), dp(50)))
                username = Label(text=invite, size_hint=(None, None), size=(dp(70), dp(50)), color=(0, 0, 0, 1))
                accept = Button(text='Accept', size_hint=(None, None), size=(dp(50), dp(50)))
                decline = Button(text='Decline', size_hint=(None, None), size=(dp(50), dp(50)))
                accept.bind(on_press=lambda instance, inv=invite: self.accept_invite(inv))
                decline.bind(on_press=lambda instance, inv=invite: self.decline_invite(inv))
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
        self.ids.friend_list.text = "Friends:\n" + self.friends
        self.parent.parent.parent.parent.ids.username.accept_invite(username)

    def decline_invite(self, username):
        self.parent.parent.parent.parent.ids.username.decline_invite(username)
        invites_list = self.invites.split(", ")
        invites_list.remove(username)
        self.invites = ", ".join(invites_list)
        self.toggle_dropdown()
        self.toggle_dropdown()
