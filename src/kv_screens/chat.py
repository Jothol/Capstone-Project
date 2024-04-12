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

from src.database import socket_client


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

    def __init__(self, session_name, username, **kwargs):
        super().__init__(**kwargs)
        # Define the characteristics of the gridlayout
        self.cols = 1
        self.rows = 3
        self.session_name = session_name
        self.username = username
        self.pos_hint = {'bottom': 1}
        self.height = Window.size[1]
        with self.canvas.before:
            self.background_color = (0, 0, 0, 1)
            self.background_fill_color = (0, 0, 0, 1)

        # Create the float layout in order for ls_tab1 to place the color option button and leave chat option
        self.chat_options = FloatLayout(size=(Window.width, 30), pos_hint={'top': 1}, size_hint=(None, None))
        # Add to ls_tab1 when chat is engaged
        self.color_options = Button(text="Color", size_hint=(None, None), size=(100, 30),
                                    pos_hint={'left': 1, 'top': 1}, background_color=(0, 1, 0, 1))
        self.leave_chat = Button(text="Leave Chat", size_hint=(None, None), size=(100, 30),
                                 pos_hint={'right': 1, 'top': 1}, background_color=(0, 1, 0, 1))
        self.chat_options.add_widget(self.color_options)
        self.chat_options.add_widget(self.leave_chat)
        self.add_widget(self.chat_options)

        # Add the scrollable history label to the grid
        self.history = ScrollableLabel(size_hint=(1, 0.7))
        self.add_widget(self.history)

        # Add the send and text input to the grid
        self.new_message = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False,
                                     height=Window.size[1] * 0.1, size_hint_y=None)
        self.send = Button(text="Send", size_hint_x=None, size_hint_y=None, height=Window.size[1] * 0.1)
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
