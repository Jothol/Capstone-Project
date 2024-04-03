import os
import sys

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import ObjectProperty, Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget

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
            button = Button(text=build_dropdown_text(self.invites), background_color=(0.1, 0.1, 0.1, 1),
                            size_hint=(None, None), size=(dp(150), dp(50)))
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
        dark = DarkenScreen()
        self.add_widget(dark)


class DarkenScreen(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dark_rectangle = Rectangle()
        self.darken()
        self.box = are_you_sure = self.create_boxlayout()
        are_you_sure.add_widget(Label(text="Delete Account", font_size=dp(20), color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(30))))
        are_you_sure.add_widget(BoxLayout(orientation="horizontal"))
        options = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint=(None, None), size=(dp(180), dp(30)))
        yes = Button(text="Delete")
        yes.bind(on_release=lambda instance: self.delete())
        no = Button(text="Cancel")
        no.bind(on_release=lambda instance: self.cancel())
        options.add_widget(yes)
        options.add_widget(no)
        are_you_sure.add_widget(options)
        self.add_widget(are_you_sure)

    def delete(self):
        account.delete_account(App.get_running_app().screen_manager.ids.username.get_username())
        App.get_running_app().logout()

    def cancel(self):
        print('accessed')
        self.parent.remove_widget(self)

    def darken(self):
        with self.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black color
            self.dark_rectangle = Rectangle(pos=self.pos, size=Window.size)

    def on_size(self, *args):
        self.dark_rectangle.size = self.size

    def on_pos(self, *args):
        self.dark_rectangle.pos = self.pos

    def on_touch_down(self, touch):
        if self.box.children[0].collide_point(*touch.pos):
            return super().on_touch_down(touch)
        else:
            return True

    def on_touch_move(self, touch):
        return True

    def on_touch_up(self, touch):
        return True

    def create_boxlayout(self):
        box_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(200), dp(150)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=dp(10)
        )

        with box_layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            box_layout.rounded_rectangle = RoundedRectangle(pos=box_layout.pos, size=box_layout.size, radius=[10])

        def update_rounded_rectangle(instance, value):
            box_layout.rounded_rectangle.size = value

        def update_rounded_rectangle_pos(instance, value):
            box_layout.rounded_rectangle.pos = value

        box_layout.bind(size=update_rounded_rectangle)
        box_layout.bind(pos=update_rounded_rectangle_pos)

        return box_layout

