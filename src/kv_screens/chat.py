import sys
import threading

from kivy.clock import Clock
from kivy.core.window import Window, Keyboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from src.database import socket_client
from src.kv_screens.hoverablebutton import HoverableButton
# from src.kv_screens.ls_tab1 import LS_Tab1


def show_error(message):
    raise Exception(message)
    # Clock.schedule_once(sys.exit, 10)


class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)

        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True, pos=self.pos,
                                  size=self.size, height=self.layout.height)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message
        if self.layout.height < self.chat_history.texture_size[1] + 15:
            self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.layout.height
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)
        self.scroll_to(self.scroll_to_point)


    def update_chat_history_layout(self, _=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)


    def update_chat_background(self, instance, value):
        self.chat_background.pos = instance.pos
        self.chat_background.size = instance.size


class ChatScreen(GridLayout):
    # color drop used to define is color dropdown is open or not and create dropdown_box object
    dropdown_open = False
    dropdown_box = None
    # chatter_color used to define chatter's chosen color
    chatter_color = "20dd20"

    def __init__(self, session_name, username, color, **kwargs):
        super().__init__(**kwargs)
        # Define the characteristics of the gridlayout
        self.users = {}
        self.cols = 1
        self.rows = 2
        self.session_name = session_name
        self.username = username
        self.height = Window.height * 0.8
        self.chatter_color = color

        with self.canvas.before:
            self.background_color = (0, 0, 0, 1)
            self.background_fill_color = (0, 0, 0, 1)

        # Create the float layout in order for ls_tab1 to place the color option button and leave chat option
        self.chat_options = FloatLayout(size=(Window.width, Window.height * 0.05), pos_hint={'top': 1}, size_hint=(None, None))

        # Create box layout to enable dropdown menu
        self.dropdown_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(100), dp(210)),
                                      pos_hint={'left': 1, 'top': 1})

        self.color_options = HoverableButton(text="Color", size_hint=(None, None), size=(dp(100), dp(30)),
                                             pos_hint={'left': 1, 'top': 1}, background_color=(0, 1, 0, 1),
                                             offset=(0, -50))
        self.color_options.bind(on_press=lambda instance: self.toggle_dropdown())
        # Bound to ls_tab1 disconnect in that file
        self.leave_chat = HoverableButton(text="Leave Chat", size_hint=(None, None), size=(dp(100), dp(30)),
                                          pos_hint={'right': 1, 'top': 1}, background_color=(0, 1, 0, 1),
                                          offset=(0, -50))
        self.chat_options.add_widget(self.color_options)
        self.chat_options.add_widget(self.leave_chat)

        # Add the scrollable history label to the grid
        self.chat_window = RelativeLayout(size_hint=(None, None), size=(Window.width, Window.height * 0.8))
        self.history = ScrollableLabel(size_hint=(None, None), height=Window.height * 0.85, width=Window.width - 100,
                                       pos_hint={'left': 1})
        self.chat_window.add_widget(self.chat_options)
        self.chat_window.add_widget(self.history)

        self.add_widget(self.chat_window)
        # self.add_widget(self.history)

        # Add the send and text input to the grid
        self.new_message = TextInput(width=(Window.width - 100) * 0.8, size_hint_x=None, multiline=False,
                                     height=Window.height * 0.1, size_hint_y=None)
        self.send = HoverableButton(text="Send", size_hint_x=None, size_hint_y=None, height=Window.height * 0.1,
                                    width=(Window.width - 100) * 0.2, offset=(0, -50))
        self.send.bind(on_press=self.send_message)

        # Create grid layout for text input and send button
        bottom_line = GridLayout(cols=2, width=Window.width - 100, height=Window.height * 0.1, size_hint=(None, None),
                                 pos_hint={'x': 0.875, 'bottom': 0.9})
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        # Bind send message to enter key
        Window.bind(on_key_down=self.on_key_down)
        self.bind(size=self.adjust_fields)

        Clock.schedule_once(self.focus_text_input, 1)
        socket_client.start_listening(self.incoming_message, show_error, self.session_name)

    def adjust_fields(self, *_):
        # Chat history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.8
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width

        # Update chat history layout
        # self.history.update_chat_history_layout()
        Clock.schedule_once(self.history.update_chat_history_layout, 0.01)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # Enter key
            self.send_message(None)
        if keycode == 43 and self.parent is not None:  # Tab key
            self.parent.parent.disconnect()

    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            self.history.update_chat_history(
                f"[color={self.chatter_color}]{self.username}[/color] >  {message}")
            socket_client.send(message)

        Clock.schedule_once(self.focus_text_input, 0.1)

    def focus_text_input(self, _):
        self.new_message.focus = True

    def incoming_message(self, username, message):
        other_color = username.split("_")[1]
        realuser = username.split("_")[0]
        if realuser == self.username:
            self.history.update_chat_history(f"[color={self.chatter_color}]{realuser}[/color] >  {message}")
        else:
            if self.users.get(realuser) is not None:
                other_color = self.users.get(realuser)
            else:
                self.users[realuser] = other_color
            self.history.update_chat_history(f"[color={other_color}]{realuser}[/color] >  {message}")

    def toggle_dropdown(self):
        if self.dropdown_open:
            # If dropdown is open remove the dropdown
            self.chat_options.remove_widget(self.dropdown_box)
            self.dropdown_open = False
        else:
            self.dropdown_box.clear_widgets()
            # Define the different colors available to select for the chat
            # dropdown_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(100), dp(210)),
            #                         pos_hint={'left': 1, 'top': 1})
            # Define the different colors available
            red_button = HoverableButton(text="Red", background_color=(0, 1, 0, 1), offset=(0, -50),
                                         size_hint=(None, None), size=(dp(100), dp(30)))
            green_button = HoverableButton(text="Green", background_color=(0, 1, 0, 1), offset=(0, -50),
                                           size_hint=(None, None), size=(dp(100), dp(30)))
            yellow_button = HoverableButton(text="Yellow", background_color=(0, 1, 0, 1), offset=(0, -50),
                                            size_hint=(None, None), size=(dp(100), dp(30)))
            blue_button = HoverableButton(text="Blue", background_color=(0, 1, 0, 1), offset=(0, -50),
                                          size_hint=(None, None), size=(dp(100), dp(30)))
            purple_button = HoverableButton(text="Purple", background_color=(0, 1, 0, 1), offset=(0, -50),
                                            size_hint=(None, None), size=(dp(100), dp(30)))
            pink_button = HoverableButton(text="Pink", background_color=(0, 1, 0, 1), offset=(0, -50),
                                          size_hint=(None, None), size=(dp(100), dp(30)))
            orange_button = HoverableButton(text="Orange", background_color=(0, 1, 0, 1), offset=(0, -50),
                                            size_hint=(None, None), size=(dp(100), dp(30)))
            red_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                            on_press=lambda instance: self.new_color("red"))
            green_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                              on_press=lambda instance: self.new_color("green"))
            yellow_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                               on_press=lambda instance: self.new_color("yellow"))
            blue_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                             on_press=lambda instance: self.new_color("blue"))
            purple_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                               on_press=lambda instance: self.new_color("purple"))
            pink_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                             on_press=lambda instance: self.new_color("pink"))
            orange_button.bind(on_release=lambda instance: self.toggle_dropdown(),
                               on_press=lambda instance: self.new_color("orange"))
            self.dropdown_box.add_widget(red_button)
            self.dropdown_box.add_widget(green_button)
            self.dropdown_box.add_widget(yellow_button)
            self.dropdown_box.add_widget(blue_button)
            self.dropdown_box.add_widget(purple_button)
            self.dropdown_box.add_widget(pink_button)
            self.dropdown_box.add_widget(orange_button)
            self.chat_options.add_widget(self.dropdown_box)
            self.dropdown_open = True

    def new_color(self, color):
        # Change the chatter color based on what was pressed in the dropdown menu
        if color == "red":
            self.chatter_color = "dd2020"
        elif color == "green":
            self.chatter_color = "00ff00"
        elif color == "yellow":
            self.chatter_color = "ffff00"
        elif color == "blue":
            self.chatter_color = "00ffff"
        elif color == "purple":
            self.chatter_color = "8a2be2"
        elif color == "pink":
            self.chatter_color = "ff00ff"
        elif color == "orange":
            self.chatter_color = "ffa500"
