import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

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

    button.bind(pos=lambda instance, value: setattr(icon, 'center', instance.center))
    button.bind(size=lambda instance, value: setattr(icon, 'center', instance.center))
    button.add_widget(icon)

    if button_type == 'accept':
        button.bind(on_press=lambda instance, inv=invite: screen.accept_invite(inv))
    elif button_type == 'decline':
        button.bind(on_press=lambda instance, inv=invite: screen.decline_invite(inv))

    return button


class Tab3(Screen):
    index = 3
    dropdown_open = False
    error_window_open = False
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
        if self.error_window_open:
            return False
        if username == "":
            self.animate_error_window('Field must not be blank.', (1, 0, 0, 1))
            return False
        elif not account.get_account(username):
            self.animate_error_window(username + ' user not found.', (1, 0, 0, 1))
            return False
        elif username in self.friends:
            self.animate_error_window('Already friends with ' + username + '.', (1, 0, 0, 1))
            return False
        self.animate_error_window('Invite sent to ' + username + '.', (0, 0.5, 0, 1))
        self.parent.parent.parent.parent.ids.username.send_invite(username)
        return True

    def remove_friend(self, username):
        if self.error_window_open:
            return False
        if username == "":
            self.animate_error_window('Field must not be blank.', (1, 0, 0, 1))
            return False
        elif not self.parent.parent.parent.parent.ids.username.remove_friend(username):
            self.animate_error_window(username + ' not in friends list.', (1, 0, 0, 1))
            return False
        self.animate_error_window(username + ' successfully unfriended.', (0, 0.5, 0, 1))
        friends_list = self.friends.split("\n")
        friends_list.remove(username)
        self.friends = "\n".join(friends_list)
        self.ids.friend_list.text = "" + self.friends
        return True

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

    def animate_error_window(self, message: str, color):
        error_window = self.ids.error_window
        message_label = self.ids.window_message
        if message != '':
            message_label.text = message
            error_window.x = dp(-200)
        if error_window.x <= dp(-7):
            self.ids.friend_input.text = ''
            self.error_window_open = True
            animation_window = Animation(pos=(error_window.x + dp(195), error_window.y), duration=0.1)
            error_window.opacity = 1
            message_label.color = color
            animation_window.start(error_window)
            Clock.schedule_once(lambda dt: self.animate_error_window('', (0, 0, 0, 0)), 5)
        else:
            self.error_window_open = False
            animation_window = Animation(pos=(error_window.x - dp(195), error_window.y), duration=0.1)
            animation_window.start(error_window)
            animation_window.bind(on_complete=lambda *args: setattr(error_window, 'opacity', 0))
            animation_window.bind(on_complete=lambda *args: setattr(message_label, 'text', ''))

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
        self.box = are_you_sure = create_boxlayout()
        are_you_sure.add_widget(Label(text="Delete Account", font_size=dp(20), color=(0, 0, 0, 1), bold=True,
                                      size_hint=(None, None), size=(dp(180), dp(30))))
        are_you_sure.add_widget(Label(text="\n*Are you sure you want to delete", color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(23)), font_size=dp(11)))
        are_you_sure.add_widget(Label(text="your account? All of your information", color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(12)), font_size=dp(11)))
        are_you_sure.add_widget(Label(text="will be permanently deleted.", color=(0, 0, 0, 1),
                                      size_hint=(None, None), size=(dp(180), dp(12)), font_size=dp(11)))
        are_you_sure.add_widget(BoxLayout(orientation="horizontal"))
        options = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint=(None, None), size=(dp(180), dp(30)))
        yes = Button(text="Delete")
        yes.bind(on_release=lambda instance: self.delete())
        no = Button(text="Cancel", background_color=(0, 1, 0, 1))
        no.bind(on_release=lambda instance: self.cancel())
        options.add_widget(yes)
        options.add_widget(no)
        are_you_sure.add_widget(options)
        self.add_widget(are_you_sure)

    def delete(self):
        account.delete_account(self.parent.parent.parent.parent.parent.ids.username.get_username())
        App.get_running_app().logout()

    def cancel(self):
        print('accessed')
        self.parent.remove_widget(self)

    def darken(self):
        with self.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black color
            self.dark_rectangle = Rectangle(pos=self.pos, size=Window.size)

    def on_size(self, *args):
        self.dark_rectangle.size = args[1]

    def on_pos(self, *args):
        self.dark_rectangle.pos = args[1]

    def on_touch_down(self, touch):
        if self.box.children[0].collide_point(*touch.pos):
            return super().on_touch_down(touch)
        else:
            return True

    def on_touch_move(self, touch):
        return True

    def on_touch_up(self, touch):
        return True


def create_boxlayout():
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

    box_layout.bind(size=lambda instance, value: setattr(box_layout.rounded_rectangle, 'size', value))
    box_layout.bind(pos=lambda instance, value: setattr(box_layout.rounded_rectangle, 'pos', value))

    return box_layout
