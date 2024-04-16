import sys
import threading

from kivy.clock import Clock
from kivy.core.window import Window, Keyboard
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from src.database import socket_client
from src.kv_screens.hoverablebutton import HoverableButton

def show_error(message):
    raise Exception(message)
    # Clock.schedule_once(sys.exit, 10)


class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        #self.layout.bind(minimum_height=self.layout.setter('height'))

        '''self.border = (0, 0, 0, 0)
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.chat_border = Rectangle(size=self.size, pos=self.size)
            Color(0, 0, 0, 1)
            self.chat_background = Rectangle(size=self.size, pos=self.pos)
        '''
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True, pos=self.pos, \
                                  size=self.size)
        # self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        # self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message
        if self.layout.height < self.chat_history.texture_size[1] + 15:
            self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.layout.height
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)


    def update_chat_history_layout(self, _=None):
        #self.layout.height = self.chat_history.texture_size[1] + 15
        #self.chat_history.height = self.chat_history.texture_size[1]
        #self.chat_history.text_size = (self.chat_history.width * 0.98, None)
        self.layout.height = self.layout.minimum_height

    def update_chat_background(self, instance, value):
        self.chat_background.pos = instance.pos
        self.chat_background.size = instance.size


class ChatScreen(GridLayout):
    # color drop used to define is color dropdown is open or not
    dropdown_open = False
    # chatter_color used to define chatter's chosen color
    chatter_color = "20dd20"

    def __init__(self, session_name, username, **kwargs):
        super().__init__(**kwargs)
        # Define the characteristics of the gridlayout
        self.cols = 1
        self.rows = 3
        self.session_name = session_name
        self.username = username
        self.height = Window.size[1]

        with self.canvas.before:
            self.background_color = (0, 0, 0, 1)
            self.background_fill_color = (0, 0, 0, 1)

        # Create the float layout in order for ls_tab1 to place the color option button and leave chat option
        self.chat_options = FloatLayout(size=(Window.width, 30), pos_hint={'top': 1}, size_hint=(None, None))
        # Add to ls_tab1 when chat is engaged
        self.color_options = HoverableButton(text="Color", size_hint=(None, None), size=(dp(100), dp(30)),
                                             pos_hint={'left': 1, 'top': 1}, background_color=(0, 1, 0, 1),
                                             offset=(0, -50))
        self.color_options.bind(on_press=lambda instance: self.toggle_dropdown())
        self.leave_chat = HoverableButton(text="Leave Chat", size_hint=(None, None), size=(dp(100), dp(30)),
                                          pos_hint={'right': 1, 'top': 1}, background_color=(0, 1, 0, 1),
                                          offset=(0, -50))
        self.chat_options.add_widget(self.color_options)
        self.chat_options.add_widget(self.leave_chat)
        self.add_widget(self.chat_options)

        # Add the scrollable history label to the grid
        self.history = ScrollableLabel(size_hint=(None, None), height=Window.size[1] * 0.65, width=Window.width)
        self.add_widget(self.history)

        # Add the send and text input to the grid
        self.new_message = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False,
                                     height=Window.size[1] * 0.1, size_hint_y=None)
        self.send = HoverableButton(text="Send", size_hint_x=None, size_hint_y=None, height=Window.size[1] * 0.1,
                                    width=Window.size[0] * 0.2, offset=(0, -50))
        self.send.bind(on_press=self.send_message)

        bottom_line = GridLayout(cols=2)
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
                f"[color=dd2020]{self.username}[/color] >  {message}")
            socket_client.send(message)

        Clock.schedule_once(self.focus_text_input, 0.1)

    def focus_text_input(self, _):
        self.new_message.focus = True

    def incoming_message(self, username, message):
        if username == self.username:
            self.history.update_chat_history(f"[color=dd2020]{username}[/color] >  {message}")
        else:
            self.history.update_chat_history(f"[color=20dd20]{username}[/color] >  {message}")

    def toggle_dropdown(self):
        if self.dropdown_open:
            # Define the different colors available to select for the chat
            red_button = HoverableButton(text="Red", background_color=(0, 1, 0, 1), offset=(0, -50),
                                         size_hint=(None, None), size=(dp(100), dp(30)),
                                         pos_hint={'left': 1, 'top': 1})
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
            red_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                            on_release=lambda instance: self.new_color("red"))
            green_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                              on_release=lambda instance: self.new_color("green"))
            yellow_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                               on_release=lambda instance: self.new_color("yellow"))
            blue_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                             on_release=lambda instance: self.new_color("blue"))
            purple_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                               on_release=lambda instance: self.new_color("purple"))
            pink_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                             on_release=lambda instance: self.new_color("pink"))
            orange_button.bind(on_press=lambda instance: self.toggle_dropdown(),
                               on_release=lambda instance: self.new_color("orange"))
            self.chat_options.add_widget(red_button)
            self.chat_options.add_widget(green_button)
            self.chat_options.add_widget(yellow_button)
            self.chat_options.add_widget(blue_button)
            self.chat_options.add_widget(purple_button)
            self.chat_options.add_widget(pink_button)
            self.chat_options.add_widget(orange_button)
            self.dropdown_open = False
        else:
            self.dropdown_open = True

    def new_color(self, color):
        # Change the chatter color based on what was pressed in the dropdown menu
        if color == "red":
            self.chatter_color = "20dd20"
        elif color == "green":
            self.chatter_color = "20dd20"
        elif color == "yellow":
            self.chatter_color = "20dd20"
        elif color == "blue":
            self.chatter_color = "20dd20"
        elif color == "purple":
            self.chatter_color = "20dd20"
        elif color == "pink":
            self.chatter_color = "20dd20"
        elif color == "orange":
            self.chatter_color = "20dd20"
