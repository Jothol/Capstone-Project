import os
import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager

from src.kv_screens.add_account_info import AddAccountInfo
from src.kv_screens.change_password import ChangePassword
from src.kv_screens.create_account import CreateAccount
from src.kv_screens.home import HomeScreen
from src.kv_screens.login import LoginScreen

import firebase_admin
from firebase_admin import credentials

from src.kv_screens.listening_session import ListeningSessionScreen

_fixed_size = (800, 600)  # desired fix size


def reSize(*args):
    Window.size = _fixed_size
    return True


Window.bind(on_resize=reSize)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
        sm.add_widget(ListeningSessionScreen(name='listening_session_page'))
        sm.add_widget(ChangePassword(name='change_password_page'))


if __name__ == '__main__':
    cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "seniorcapstone-musicapp-675df",
  "private_key_id": "380b5390006b1d9873dab8a220cb8a5e0cf029e0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDC5tQb+wFWM6KQ\nkbXIANBa4XxA6ViKc9RgzT/eHUFt+J/3YKt5tUURBut/Fc3t9GV9OgjoK4n07+V0\nLHxROfgPhKUYY40wDHCrmsr/CnnJAZx2Wt/iuvSSJqJZvGyn9GJ/MBlLzIKMNHG4\n6Rx+SDewnP5ALPkRaBXEAqHF50Clk/pt0pU1MKzioZVqZBQ5EII29dS5tqwNaniF\nyATyGqRhFsWmB06WhTdHB+N2l2Q2UhRYiB+DNvlwM9CcySO8QZD7AkrhpJh0UqM7\njVeQCTIzn7GumEmbxXqf/bSbXUZAJjsSu08pXRq4Ia/Ec5Qd2fvFr5bTNrf3cTuw\nveJaRj19AgMBAAECggEAHREr5RhkNKTyw7jXcYKdkFA8pbmnWM65h85Ujh2y2mHQ\nCabDLB2atVVg3c00rx5Z3HlBRs7nfj4g7FiOGdcZZccUkDSYo+fXDeDCEZNQYmf5\nG7Wl2jyjqQBWCigN1GagIfPcce+IMLzJkRhDBZpjo9VmHdAXPT9Wr6rs0YURoR/T\n25ik9jjEdji1/twOHB+uacvP72xCtLG2eandxqD6XqJKnNHf8OJqV8pTDJ85byrg\nxywCL8g+jSnfchruHHQ4wfcSMxSUwE1zCpmrxHzHZ6YuRYYPhWhP+fa8yHj3VED+\nka9jN9v2UcayBdmuxgSdDqsRGBRsqIPpHGHT+9ssCQKBgQDvEoVqx425949DHb4E\n71FPydpNsEJn/TqpqUGarVfrC4G2gpg1ViVqYfd4IiJAE41lVaNruzQmqZbpUudI\nnneF1Oyd+r5tB1vS61Sf63EgO4hNhBeEZgCmUEFv46YZQMrkDHN9MlXh7HkDWK7i\nLP9KAXsjegU4ZPIHwtDcppK1ewKBgQDQs6jte663pWw03vScMi35jQ5ICgZ3RQf3\nNp3LAjafklSKvDmYQzGQzho+1Mp5F5ozpV4Xrs2Xs8vFZZVeqxy52BbtpPrQM8Fz\npR398B4EwdUgtA3q41ItW1iP9inm0tJwdx3WR7iJXmlzkfbB+md5XiholGZVlpFj\nzPOqWk3bZwKBgQDqdw2mBYP3yNUWC8taZ6MlT1/sJVtbRT0NO9P9cNfyytwyNK42\nUQBs7xuXFFLm6MYZhf26IGUrLdO1jPsLe27ZMFPHNC0iHL9vgiECnhPaeshYzZ2K\n2cb1VWx34Zn61lKliZiSRpV390VPhOAvLdZJrF4qEvefsVC1T9krLapglQKBgQCR\nRe352VVGKlUG/IeCzn8oLaLaTHgxv5CK6a6u6EyDiQVmSR1COsuew4iLYe3Kmr5Q\n4vR7QceEqLfYIRz3d96YEq3rICMimFQ5np8g62rJ3u7vQ8ZIUZIbVnFwTGbgcLHh\nbVkMloICxQBcXSdJ4XbzibJREbOmMhfkQ379fryhUwKBgCaZ5egyc7YWGy8ZZzhD\nXSMPcLPMf3Trd+vf0Sf4ojH7ZmCttb34uOBSyg6HQtv+Vdl5Zei6QX9kkY9YvBCY\n41OfmoAd9xF8IbLW+mORJxRAqORmn7jys0vFa1M1gqFhIzr9z2MqoJbQG0g+dAQc\nTy7M1REx+etpFMq/WzIV6FmI\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-2p3od@seniorcapstone-musicapp-675df.iam.gserviceaccount.com",
  "client_id": "112161044479444019787",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2p3od%40seniorcapstone-musicapp-675df.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
    firebase_admin.initialize_app(cred)

    Builder.load_string("""#:kivy 2.3.0
# create_account.kv
#:import HoverableButton src.database.hoverablebutton

<LoginScreen>:
    Image:
        source: '../other/images/temp_logo.png'
        fit_mode: 'scale-down'

    BoxLayout:
        orientation: 'vertical'

        Label:
            text: 'Listen together with SpotiVibe.'
            size_hint: (None, None)
            size: (dp(600), dp(40))
            font_size: dp(20)
            bold: True
            pos_hint: {'center_x': 0.5}

        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'

            BoxLayout:
                orientation: 'vertical'
                size_hint: (None, None)
                size: (dp(250), dp(250))
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10), dp(10), dp(10), dp(10)]

                Label:
                    text: 'SpotiVibe Log-In.'
                    color: [0,0.4,0,1]
                    font_size: dp(20)
                    bold: True
                BoxLayout:
                    padding: dp(10)

                    TextInput:
                        id: username_input
                        multiline: False
                        hint_text: 'Username'
                        write_tab: False
                        on_text_validate: root.submit(username_input.text, password_input.text)

                BoxLayout:
                    padding: dp(10)

                    TextInput:
                        id: password_input
                        multiline: False
                        hint_text: 'Password'
                        password: True
                        write_tab: False
                        on_text_validate: root.submit(username_input.text, password_input.text)

                AnchorLayout:
                    anchor_x: 'center'
                    anchor_y: 'center'

                    HoverableButton:
                        id: login_submit_button
                        size_hint: (None, None)
                        size: (dp(130), dp(30))
                        text: 'Enter'
                        background_color:[0,1,0,1]
                        on_press:
                            root.manager.transition.direction = 'down'
                            root.submit(username_input.text, password_input.text)
                Label:
                    id: error_message
                    text: ''
                    color: [1,0,0,0]

        HoverableButton:
            size_hint: (None, None)
            size: (dp(130), dp(30))
            text: 'Create Account'
            pos_hint: {'x': 0.01, 'y': 0.01}
            background_color:[0,1,0,1]
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'create_account_page'""")
    Builder.load_string("""# create_account.kv
#:import HoverableButton src.database.hoverablebutton

<CreateAccount>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (dp(250), dp(300))
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10), dp(10), dp(10), dp(10)]

            Label:
                text: 'Welcome to SpotiVibe!'
                color: [0,0.4,0,1]
                font_size: dp(20)
                bold: True
            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: username_input
                    multiline: False
                    hint_text: 'Username'
                    write_tab: False
                    on_text_validate: root.submit(username_input.text, password_input.text, re_password_input.text)

            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: password_input
                    multiline: False
                    hint_text: 'Password'
                    password: True
                    write_tab: False
                    on_text_validate: root.submit(username_input.text, password_input.text, re_password_input.text)

            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: re_password_input
                    multiline: False
                    hint_text: 'Re-enter Password'
                    password: True
                    write_tab: False
                    on_text_validate: root.submit(username_input.text, password_input.text, re_password_input.text)

            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'center'

                HoverableButton:
                    size_hint: (None, None)
                    size: (dp(130), dp(30))
                    text: 'Create Account'
                    background_color:[0,1,0,1]
                    on_press:
                        root.manager.transition.direction = 'left'
                        root.submit(username_input.text, password_input.text, re_password_input.text)
            Label:
                id: error_message
                text: ''
                color: [1,0,0,0]

    HoverableButton:
        size_hint: (None, None)
        size: (dp(100), dp(30))
        text: 'Go Back'
        pos_hint: {'x': 0.01, 'y': 0.01}
        background_color:[0,1,0,1]
        on_press:
            root.manager.transition.direction = 'right'
            root.manager.current = 'login_page'""")
    Builder.load_string("""# create_account.kv
#:import HoverableButton src.database.hoverablebutton

<AddAccountInfo>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (dp(250), dp(300))
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10), dp(10), dp(10), dp(10)]

            Label:
                text: 'Add Account Info'
                color: [0,0.4,0,1]
                font_size: dp(20)
                bold: True
            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: email_input
                    multiline: False
                    hint_text: 'Email'
                    write_tab: False
                    on_text_validate: root.submit(email_input.text, first_name_input.text, last_name_input.text)

            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: first_name_input
                    multiline: False
                    hint_text: 'First Name'
                    write_tab: False
                    on_text_validate: root.submit(email_input.text, first_name_input.text, last_name_input.text)

            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: last_name_input
                    multiline: False
                    hint_text: 'Last Name'
                    write_tab: False
                    on_text_validate: root.submit(email_input.text, first_name_input.text, last_name_input.text)

            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'center'

                HoverableButton:
                    size_hint: (None, None)
                    size: (dp(130), dp(30))
                    text: 'Update Info'
                    background_color:[0,1,0,1]
                    on_press:
                        root.manager.transition.direction = 'down'
                        root.submit(email_input.text, first_name_input.text, last_name_input.text)
            Label:
                id: error_message
                text: ''
                color: [1,0,0,0]

    HoverableButton:
        size_hint: (None, None)
        size: (dp(100), dp(30))
        text: 'Add Later'
        pos_hint: {'x': 0.01, 'y': 0.01}
        background_color:[0,1,0,1]
        on_press:
            root.manager.transition.direction = 'down'
            root.manager.current = 'home_page'""")
    Builder.load_string("""#:import HoverableButton src.database.hoverablebutton

<ChangePassword>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (dp(250), dp(250))
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10), dp(10), dp(10), dp(10)]

            Label:
                text: 'Change Password'
                color: [0,0.4,0,1]
                font_size: dp(20)
                bold: True
            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: password_input
                    multiline: False
                    hint_text: 'Password'
                    password: True


            BoxLayout:
                padding: dp(10)

                TextInput:
                    id: re_password_input
                    multiline: False
                    hint_text: 'Re-enter Password'

            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'center'

                HoverableButton:
                    size_hint: (None, None)
                    size: (dp(130), dp(30))
                    text: 'Update Password'
                    background_color:[0,1,0,1]
                    on_press:
                        root.manager.transition.direction = 'down'
                        root.submit(password_input.text, re_password_input.text)
            Label:
                id: error_message
                text: ''
                color: [1,0,0,0]

    HoverableButton:
        size_hint: (None, None)
        size: (dp(100), dp(30))
        text: 'Cancel'
        pos_hint: {'x': 0.01, 'y': 0.01}
        background_color:[0,1,0,1]
        on_press:
            root.manager.transition.direction = 'down'
            root.manager.current = 'home_page'""")
    Builder.load_string("""#:kivy 2.3.0
#:import HoverableButton src.database.hoverablebutton

<HomeScreen>:
    BoxLayout:
        id: background_image_container
        orientation: 'vertical'

        Image:
            source: '../other/images/temp_logo.png'
            fit_mode: 'scale-down'


<TabBar>:
    id: tab_bar
    size_hint_y: None
    height: dp(50)  # Set the height in dp (adjust as needed)

    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1  # Dark grey color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0, 0, 0, 1  # Dark grey color
        Line:
            width: 1
            points: [self.width / 2, 0, self.width / 2, self.height]
        # Line:
        #     width: 1
        #     points: [2 * self.width / 3, 0, 2 * self.width / 3, self.height]

    Button:
        id: home_button
        size_hint: None, None  # Disable the x-size hint
        size: dp(50), dp(50)  # Set the width in dp (adjust as needed)
        pos_hint: {'center_x': 1/4, 'center_y': 0.5}
        background_color: 0, 0, 0, 0

        on_press:
            root.switch_screen('1')

        Image:
            id: home_image
            source: '../other/images/home_icon.png'
            center: self.parent.center
            size: self.parent.height * 0.8, self.parent.height * 0.8
            canvas.after:
                Color:
                    rgba: 0, 1, 0, 0.5  # Red tint with 50% opacity
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: self.source

    #Button:
    #    id: search_button
    #    size_hint: None, None  # Disable the x-size hint
    #    size: dp(50), dp(50)  # Set the width in dp (adjust as needed)
    #    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    #    background_color: 0, 0, 0, 0
#
    #    on_press:
    #        root.switch_screen('2')
#
    #    Image:
    #        id: search_image
    #        source: '../other/images/search_icon.png'
    #        center: self.parent.center
    #        size: self.parent.height * 0.5, self.parent.height * 0.5
    #        canvas.after:
    #            Color:
    #                rgba: 0, 1, 0, 0  # Red tint with 50% opacity
    #            Rectangle:
    #                pos: self.pos
    #                size: self.size
    #                source: self.source

    Button:
        id: setting_button
        size_hint: None, None  # Disable the x-size hint
        size: dp(50), dp(50)  # Set the width in dp (adjust as needed)
        pos_hint: {'center_x': 3/4, 'center_y': 0.5}
        background_color: 0, 0, 0, 0

        on_press:
            root.switch_screen('3')

        Image:
            id: settings_image
            source: '../other/images/settings_icon.png'
            size: self.parent.height * 0.5, self.parent.height * 0.5
            center: self.parent.center
            canvas.after:
                Color:
                    rgba: 0, 1, 0, 0  # Red tint with 50% opacity
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: self.source
""")
    Builder.load_string("""#:kivy 2.3.0
#:import HoverableButton src.database.hoverablebutton

<ListeningSessionScreen>:
    BoxLayout:
        id: background_image_container
        orientation: 'vertical'

    Label:
        id: session_label
        size_hint: (None, None)
        size: dp(600), dp(40)
        font_size: 20
        pos_hint: {'center_x': 0.9, 'y': 0.12}
        bold: True

    Label:
        id: user_label
        size_hint: (None, None)
        size: dp(600), dp(40)
        font_size: 20
        pos_hint: {'center_x': 0.9, 'y': 0.09}
        bold: True

    HoverableButton:
        size_hint: (None, None)
        size: (130, 30)
        text: 'Leave'
        pos_hint: {'x': 0.01, 'y': 0.09}
        background_color:[0,1,0,1]
        on_press:
            root.manager.transition.direction = 'up'
            root.submit()

    Label:
        id: error_message
        text: ''
        color: [1,0,0,0]

    BoxLayout:
        id: error_window
        size_hint: None, None
        size: self.minimum_size[0], dp(40)
        pos: dp(400), dp(500)
        opacity: 0
        padding: dp(10)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [5, 5, 5, 5]
        Label:
            id: window_message
            text: ''
            color: (0, 0, 0, 1)
            size_hint: None, None
            size: self.texture_size[0], dp(20)
            center: self.parent.center

<TabBar2>:
    size_hint_y: None
    height: dp(50)  # Set the height in dp (adjust as needed)

    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1  # Dark grey color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0, 0, 0, 1  # Dark grey color
        Line:
            width: 1
            points: [self.width / 3, 0, self.width / 3, self.height]
        Line:
            width: 1
            points: [2 * self.width / 3, 0, 2 * self.width / 3, self.height]


    Button:
        id: chat_button
        size_hint: None, None  # Disable the x-size hint
        size: dp(50), dp(50)  # Set the width in dp (adjust as needed)
        pos_hint: {'center_x': 1/6, 'center_y': 0.5}
        background_color: 0, 0, 0, 0

        on_press:
            root.switch_screen('1')

        Image:
            id: chat_image
            source: '../other/images/chat_icon.png'
            center: self.parent.center
            size: self.parent.height * 0.8, self.parent.height * 0.8
            canvas.after:
                Color:
                    rgba: 0, 1, 0, 0.5  # Red tint with 50% opacity
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: self.source

    Button:
        id: music_button
        size_hint: None, None  # Disable the x-size hint
        size: dp(50), dp(50)  # Set the width in dp (adjust as needed)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        background_color: 0, 0, 0, 0

        on_press:
            root.switch_screen('2')

        Image:
            id: music_image
            source: '../other/images/music_icon.png'
            center: self.parent.center
            size: self.parent.height * 0.5, self.parent.height * 0.5
            canvas.after:
                Color:
                    rgba: 0, 1, 0, 0  # Red tint with 50% opacity
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: self.source

    Button:
        id: setting_button
        size_hint: None, None  # Disable the x-size hint
        size: dp(50), dp(50)  # Set the width in dp (adjust as needed)
        pos_hint: {'center_x': 5/6, 'center_y': 0.5}
        background_color: 0, 0, 0, 0

        on_press:
            root.switch_screen('3')

        Image:
            id: settings_image
            source: '../other/images/settings_icon.png'
            size: self.parent.height * 0.5, self.parent.height * 0.5
            center: self.parent.center
            canvas.after:
                Color:
                    rgba: 0, 1, 0, 0  # Red tint with 50% opacity
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: self.source

#bl2 = BoxLayout(orientation='horizontal', pos=(dp(self.width / 5), dp(400)))
<HostBar>:
    size_hint_y: None
    id: host_bar
    size: self.width, dp(50)
    pos_hint: {'top': 1}
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    HoverableButton:
        id: invite_button
        text: 'Invite User'
        size_hint: None, None
        size: dp(130), dp(30)
        background_color: [0, 1, 0, 1]
        pos: (root.width / 2 - (5 * self.width / 2), self.y)
        on_press:
            root.open_bar('Invite User')
    HoverableButton:
        id: remove_button
        text: 'Remove User'
        size_hint: None, None
        size: dp(130), dp(30)
        background_color: [0, 1, 0, 1]
        pos: (root.width / 2 - (3 * self.width / 2), self.y)
        on_press:
            root.open_bar('Remove User')
    HoverableButton:
        id: new_host_button
        text: 'New Host'
        size_hint: None, None
        size: dp(130), dp(30)
        background_color: [0, 1, 0, 1]
        pos: (root.width / 2 - self.width / 2, self.y)
        on_press:
            root.open_bar('New Host')
    HoverableButton:
        id: end_session_button
        text: 'End Session'
        size_hint: None, None
        size: dp(130), dp(30)
        background_color: [0, 1, 0, 1]
        pos: (root.width / 2 + self.width / 2, self.y)
        on_press:
            root.end_session()
    HoverableButton:
        id: status
        text: 'Private'
        size_hint: None, None
        size: dp(130), dp(30)
        transition_color: "red"
        background_color: [1, 0, 0.4, 1]
        pos: (root.width / 2 + (3 * self.width / 2), self.y)
        on_press:
            root.change_status()
            root.change_hover_button()

<HostDropBar>:
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: dp(400), dp(30)
        pos_hint: {'center_x': .5, 'top': .9175}
        pos: root.width /2 - self.width / 2, self.y
        canvas.before:
            # Color:
            #     rgba: 1, 1, 1, 1
            # Line:
            #     width: dp(1)
            #     rectangle: self.x, self.y, self.width, self.height
            Color:
                rgba: 0.2, 0.2, 0.2, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            id: input_label
            text: ''
            color: [1,1,1,1]
            font_size: 20
            bold: True
        TextInput:
            id: entry
            multiline: False
            hint_text: '(User Name)'
        HoverableButton:
            id: button_input
            pos_hint: {'center_y': .5}
            text: 'Enter'
            background_color:[0,1,0,1]
            on_press:
                root.submit(entry.text)""")
    Builder.load_string("""#:import HoverableButton src.database.hoverablebutton

<Tab1>
    BoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        Label:
            id: welcome_label
            font_size: dp(30)
            bold: True
            text: 'Welcome!'
            size_hint_y: None
            height: self.texture_size[1]
            color: [1, 1, 1, 1]
        FloatLayout:
            HoverableButton:
                id: create_session
                size_hint: None, None
                size: dp(200), dp(75)
                offset: 0, -50
                pos_hint: {'center_x': 0.3, 'center_y': 0.5}
                text: 'Create Session'
                background_color: 0, 1, 0, 1
                on_press: root.create_session(True)
            HoverableButton
                id: join_session
                size_hint: None, None
                size: dp(200), dp(75)
                offset: 0, -50
                pos_hint: {'center_x': 0.7, 'center_y': 0.5}
                text: 'Join Session'
                background_color: 0, 1, 0, 1
                on_press: root.join_session(True)
    FloatLayout:
        id: create_session_window
        pos_hint: {'center_x': -0.5}
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.5
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (dp(250), dp(300))
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10), dp(10), dp(10), dp(10)]
            FloatLayout:
                size_hint: None, None
                size: dp(250), dp(25)
                Label:
                    text: 'Create a Session'
                    color: [0,0.4,0,1]
                    font_size: dp(20)
                    bold: True
                    size_hint: None, None
                    size: self.texture_size
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                Button:
                    size_hint: None, None  # Disable the x-size hint
                    size: dp(20), dp(20)  # Set the width in dp (adjust as needed)
                    pos_hint: {'center_x': 0.92, 'center_y': 0.9}
                    background_color: 0, 0, 0, 0
                    on_press: root.create_session(False)
                    Image:
                        source: '../other/images/exit_icon.png'
                        center: self.parent.center
                        size: self.parent.height * 0.5, self.parent.height * 0.5
            Label:
                text: 'Room code:'
                color: 0, 0, 0, 1
                size_hint: None, None
                size: self.texture_size
            TextInput:
                id: room_code_input
                size_hint_y: None
                height: dp(30)
                multiline: False
                hint_text: 'Code'
                write_tab: False
            Label:
                text: 'Listen with:'
                color: 0, 0, 0, 1
                size_hint: None, None
                size: self.texture_size
            ScrollView:
                size_hint_y: None
                height: dp(75)
                scroll_wheel_distance: dp(20)
                bar_width: dp(4)
                bar_margin: dp(4)
                do_scroll_x: False
                do_scroll_y: True
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1  # Red color for the border
                    Line:
                        rectangle: self.x, self.y, self.width, self.height
                        width: 1

                GridLayout:
                    id: scroll_contents
                    cols: 1
                    spacing: dp(1)
                    size_hint_y: None
                    height: self.minimum_height
            HoverableButton:
                size_hint: (None, None)
                size: (dp(130), dp(30))
                offset: 0, -50
                pos_hint: {'center_x': 0.5}
                text: 'Create Session'
                background_color:[0,1,0,1]
                on_press: root.submit(root.ids.room_code_input.text, 'Create')
            Label:
                id: error_message
                text: ''
                color: 1, 0, 0, 1
            BoxLayout:
                id: blank_space
    FloatLayout:
        id: join_session_window
        pos_hint: {'center_x': -0.5}
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.5
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (dp(250), dp(300))
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10), dp(10), dp(10), dp(10)]
            FloatLayout:
                size_hint: None, None
                size: dp(250), dp(25)
                Label:
                    text: 'Join a Session'
                    color: [0,0.4,0,1]
                    font_size: dp(20)
                    bold: True
                    size_hint: None, None
                    size: self.texture_size
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                Button:
                    size_hint: None, None  # Disable the x-size hint
                    size: dp(20), dp(20)  # Set the width in dp (adjust as needed)
                    pos_hint: {'center_x': 0.92, 'center_y': 0.9}
                    background_color: 0, 0, 0, 0
                    on_press: root.join_session(False)
                    Image:
                        source: '../other/images/exit_icon.png'
                        center: self.parent.center
                        size: self.parent.height * 0.5, self.parent.height * 0.5
            Label:
                text: 'Room code:'
                color: 0, 0, 0, 1
                size_hint: None, None
                size: self.texture_size
            TextInput:
                id: room_code_input_2
                size_hint_y: None
                height: dp(30)
                multiline: False
                hint_text: 'Code'
                write_tab: False
            HoverableButton:
                size_hint: (None, None)
                size: (dp(130), dp(30))
                pos_hint: {'center_x': 0.5}
                offset: 0, -50
                text: 'Join Session'
                background_color:[0,1,0,1]
                on_press: root.submit(root.ids.room_code_input_2.text, 'Join')
            Label:
                text: 'Session Invites:'
                color: 0, 0, 0, 1
                size_hint: None, None
                size: self.texture_size
            ScrollView:
                size_hint_y: None
                height: dp(75)
                scroll_wheel_distance: dp(20)
                bar_width: dp(4)
                bar_margin: dp(4)
                do_scroll_x: False
                do_scroll_y: True
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1  # Red color for the border
                    Line:
                        rectangle: self.x, self.y, self.width, self.height
                        width: 1

                GridLayout:
                    id: scroll_contents_2
                    cols: 1
                    spacing: dp(1)
                    size_hint_y: None
                    height: self.minimum_height
            Label:
                id: error_message
                text: ''
                color: 1, 0, 0, 1
            BoxLayout:
                id: blank_space

<Option>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(25)
    padding: dp(10)
    Label:
        id: option_label
        text: ''
        color: 0, 0, 0, 1
        opacity: 0.4
        size_hint: None, None
        width: self.texture_size[0]
        pos_hint: {'center_y': 0.5}
    BoxLayout:
        id: blank_space
    Button:
        size_hint: None, None
        size: dp(25), dp(25)
        pos_hint: {'center_y': 0.5}
        background_color: 0, 0, 0, 0

        on_press:
            root.add(self.parent.ids.option_label.text)

        Image:
            id: add_image
            source: '../other/images/accept_icon.png'
            center: self.parent.center
            size: self.parent.height * 0.6, self.parent.height * 0.6

<Option2>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(25)
    padding: dp(10)
    Label:
        id: option_label_2
        text: ''
        color: 0, 0, 0, 1
        opacity: 0.4
        size_hint: None, None
        width: self.texture_size[0]
        pos_hint: {'center_y': 0.5}
    BoxLayout:
        id: blank_space
    Button:
        size_hint: None, None
        size: dp(50), dp(20)
        font_size: dp(12)
        text: 'Join'
        pos_hint: {'center_y': 0.5}
        background_color: 0, 1, 0, 1

        on_press:
            root.join_session()

""")
    Builder.load_string("""#:import HoverableButton src.database.hoverablebutton

<Tab3>:
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(10)
            AnchorLayout:
                anchor_x: 'left'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(30)
                Label:
                    text: 'Friends:'
                    font_size: dp(30)
                    size_hint: None, None
                    size: self.texture_size
            AnchorLayout:
                anchor_x: 'left'  # Aligns children to the left
                anchor_y: 'top'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(150)
                padding: dp(10)
                canvas.before:
                    Color:
                        rgba: 0.1, 0.1, 0.1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1, 1, 1, 1
                    Line:
                        width: dp(1)
                        rectangle: self.x, self.y, self.width, self.height
                Label:
                    id: friend_list
                    size_hint: None, None
                    size: self.texture_size
                    text: "<loading>"
            AnchorLayout:
                anchor_x: 'center'  # Aligns children to the left
                anchor_y: 'top'
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(5)
                        TextInput:
                            id: friend_input
                            size_hint: None, None
                            size: dp(150), dp(30)
                            multiline: False
                            hint_text: 'Username'
                        BoxLayout:
                            size_hint: None, None
                            size: dp(150), dp(10)
                        HoverableButton:
                            text: 'Send Friend Request'
                            size_hint: None, None
                            size: dp(150), dp(30)
                            offset: 0, -50
                            background_color:[0,1,0,1]
                            on_press: root.invite_friend(friend_input.text)
                        HoverableButton:
                            text: 'Remove Friend'
                            size_hint: None, None
                            size: dp(150), dp(30)
                            offset: 0, -50
                            background_color:[0,1,0,1]
                            on_press: root.remove_friend(friend_input.text)
                        BoxLayout:
                            id: blank_space
                            orientation: 'vertical'
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: None
                        width: self.minimum_size[0]
                        BoxLayout:
                            id: dropdown_box
                            canvas.before:
                                Color:
                                    rgba: 1, 1, 1, 1  # White color
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                            orientation: 'vertical'
                            size_hint: None, None
                            size: self.minimum_size
                            HoverableButton:
                                text: 'Pending Invites'
                                size_hint: None, None
                                size: dp(150), dp(50)
                                offset: 0, -50
                                transition_color: "darkgrey"
                                background_color: (0.1, 0.1, 0.1, 1)
                                on_press:
                                    root.toggle_dropdown()
                        BoxLayout:
                            id: blank_space
                            orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(10)
            AnchorLayout:
                anchor_x: 'left'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(30)
                Label:
                    text: 'Account:'
                    font_size: dp(30)
                    size_hint: None, None
                    size: self.texture_size
            AnchorLayout:
                anchor_x: 'left'  # Aligns children to the left
                anchor_y: 'top'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(150)
                padding: dp(10)
                canvas.before:
                    Color:
                        rgba: 0.1, 0.1, 0.1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1, 1, 1, 1
                    Line:
                        width: dp(1)
                        rectangle: self.x, self.y, self.width, self.height
                Label:
                    id: account_info
                    size_hint: None, None
                    size: self.texture_size
                    text: "<loading>"
            AnchorLayout:
                anchor_x: 'center'  # Aligns children to the left
                anchor_y: 'top'
                BoxLayout:
                    id: account_management
                    orientation: 'vertical'
                    size_hint_x: None
                    width: self.minimum_size[0]
                    spacing: dp(5)
                    HoverableButton:
                        text: 'Edit Account Info'
                        size_hint: None, None
                        size: dp(150), dp(30)
                        offset: 0, -50
                        background_color:[0,1,0,1]
                        on_press:
                            root.parent.parent.parent.parent.transition.direction = 'up'
                            root.parent.parent.parent.parent.current = 'add_account_info_page'
                    HoverableButton:
                        text: 'Change Password'
                        size_hint: None, None
                        size: dp(150), dp(30)
                        offset: 0, -50
                        background_color:[0,1,0,1]
                        on_press:
                            root.parent.parent.parent.parent.transition.direction = 'up'
                            root.parent.parent.parent.parent.current = 'change_password_page'
                    BoxLayout:
                        id: blank_space
                        orientation: 'vertical'
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'bottom'
        padding: dp(10)
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(5)
            size_hint: None, None
            size: self.minimum_size
            HoverableButton:
                text: 'Logout'
                size_hint: None, None
                size: dp(120), dp(30)
                offset: 0, -50
                background_color:[0,1,0,1]
                on_press:
                    root.logout()
            HoverableButton:
                id: delete_account
                text: 'Delete Account'
                size_hint: None, None
                offset: 0, -50
                size: dp(120), dp(30)
                background_color:[0,1,0,1]
                on_press:
                    root.delete_account()
    BoxLayout:
        id: error_window
        size_hint: None, None
        size: self.minimum_size[0], dp(40)
        pos: -self.minimum_size[0], dp(10)
        opacity: 0
        padding: dp(10)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [5, 5, 5, 5]
        Label:
            id: window_message
            text: ''
            color: (0, 0, 0, 1)
            size_hint: None, None
            size: self.texture_size[0], dp(20)
            center: self.parent.center
""")
    Builder.load_string("""#:import HoverableButton src.database.hoverablebutton

<LS_Tab1>
    add_button:add_button.__self__
    HoverableButton:
        id: add_button
        size_hint: (None, None)
        size: (130, 30)
        offset: 0, -50
        text: 'Connect to Chat'
        background_color: (0, 1, 0, 1)
        pos_hint: {'x': 0.01, 'y': 0.08}
        on_press:
            root.connect()
    Label:
        id: welcome_label
        text: ""
        height: dp(300)
        bold: True
        font_size: 50
        size: dp(600), dp(40)
        pos_hint: {'center_y': .85}""")
    Builder.load_string("""#:import HoverableButton src.database.hoverablebutton

<LsTab2>:
    Image:
        id: background_image
        source: '../other/images/transparent_logo.png'
        fit_mode: 'scale-down'
        z: -1

    FloatLayout:
        BoxLayout:
            id: volume_box
            size_hint: (None, None)
            size: (dp(100), dp(80))
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}

            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10, 10, 10, 10]

            Label:
                text: 'Volume'
                color: [0,0,0,1]

        FloatLayout:
            id: player_window
            size_hint: None, None
            size: dp(500), dp(500)
            pos: (root.width - self.width) / 2, dp(-435)

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10, 10, 10, 10]
            Image:
                id: play_icon
                source: '../other/images/play_icon.png'
                size_hint: None, None
                size: dp(200), dp(200)
                pos: (root.width - self.width) / 2, self.parent.pos[1] + dp(200)
                canvas.before:
                    Color:
                        rgba: 0.8, 0.8, 0.8, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size

            Button:
                size_hint: None, None
                minimum_height: dp(10)
                size: dp(30), dp(10)
                pos: (root.width - self.width) / 2, self.parent.pos[1] + dp(485)
                background_color: 0, 0, 0, 0

                on_press: root.animate_player()
                canvas.before:
                    Color:
                        rgba: 0.3, 0.3, 0.3, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [3, 3, 3, 3]
            BoxLayout:
                id: control_buttons
                orientation: 'horizontal'
                size_hint: None, None
                size: self.minimum_size
                padding: 10
                spacing: 15

                pos: (root.width - self.width) / 2, self.parent.pos[1] + dp(435)

                Button:
                    size_hint: None, None
                    size: dp(20), dp(20)
                    pos_hint: {'center_y': 0.5}
                    background_color: 0, 0, 0, 0

                    on_press: root.dislike()

                    Image:
                        id: dislike_icon
                        source: '../other/images/dislike_icon.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y - self.parent.height / 10
                        size: self.parent.height, self.parent.height
                Button:
                    size_hint: None, None
                    size: dp(30), dp(30)
                    background_color: 0, 0, 0, 0

                    on_press: root.restart()

                    Image:
                        id: restart_icon
                        source: '../other/images/restart_icon.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: self.parent.height, self.parent.height
                Button:
                    size_hint: None, None
                    size: dp(30), dp(30)
                    background_color: 0, 0, 0, 0

                    on_press: root.play()

                    Image:
                        id: play_icon
                        source: '../other/images/play_icon.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: self.parent.height, self.parent.height
                Button:
                    size_hint: None, None
                    size: dp(30), dp(30)
                    background_color: 0, 0, 0, 0

                    on_press: root.skip()

                    Image:
                        id: skip_icon
                        source: '../other/images/skip_icon.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: self.parent.height, self.parent.height
                Button:
                    size_hint: None, None
                    size: dp(20), dp(20)
                    pos_hint: {'center_y': 0.5}
                    background_color: 0, 0, 0, 0

                    on_press: root.like()

                    Image:
                        id: like_icon
                        source: '../other/images/like_icon.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y + self.parent.height / 10
                        size: self.parent.height, self.parent.height""")
    Builder.load_string("""#:import HoverableButton src.database.hoverablebutton

<LS_Tab3>
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(5)
            AnchorLayout:
                anchor_x: 'left'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(30)
                Label:
                    text: 'Users in Session:'
                    font_size: dp(30)
                    size_hint: None, None
                    size: self.texture_size
            AnchorLayout:
                anchor_x: 'left'  # Aligns children to the left
                anchor_y: 'top'
                size_hint: None, .5
                size: self.parent.width - dp(60), dp(150)
                padding: dp(10)
                canvas.before:
                    Color:
                        rgba: 0.1, 0.1, 0.1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1, 1, 1, 1
                    Line:
                        width: dp(1)
                        rectangle: self.x, self.y, self.width, self.height
                Label:
                    id: accs_list
                    size_hint: None, None
                    size: self.parent.width, self.parent.height
                    text_size: self.width, self.height
                    text: ""
                    valign: 'top'
                    halign: 'left'
                    markup: True
                    canvas.before:
                        Color:
                            rgba: 0, 0, 0, 1
                        Line:
                            rectangle: self.parent.x, self.parent.y, self.width, self.height
                            width: 1
            BoxLayout:
                orientation: 'vertical'
                # spacing: dp(10)
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(1)
                    BoxLayout:
                        id: blank_space
                        orientation: 'vertical'
                    TextInput:
                        id: friend_input
                        size_hint: None, None
                        size: dp(150), dp(30)
                        multiline: False
                        hint_text: 'Username'
                    HoverableButton:
                        text: 'Send Friend Request'
                        size_hint: None, None
                        offset: 0, -50
                        size: dp(150), dp(30)
                        background_color:[0,1,0,1]
                        on_press: root.send_friend_request(friend_input.text)
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_x: None
                    width: self.minimum_size[0]
                    BoxLayout:
                        id: blank_space
                        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(10)
            AnchorLayout:
                anchor_x: 'left'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(30)
                Label:
                    text: 'Played Songs:'
                    font_size: dp(30)
                    size_hint: None, None
                    size: self.texture_size
            AnchorLayout:
                anchor_x: 'left'
                anchor_y: 'top'
                size_hint: None, None
                size: self.parent.width - dp(60), dp(150)
                padding: dp(5)
                canvas.before:
                    Color:
                        rgba: 0.1, 0.1, 0.1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1, 1, 1, 1
                    Line:
                        width: dp(1)
                        rectangle: self.x, self.y, self.width, self.height
                ScrollView:
                    id: scroll_id
                    size_hint_y: None
                    height: dp(135) # 35
                    scroll_wheel_distance: dp(2)
                    bar_margin: dp(10)
                    bar_width: dp(10)
                    do_scroll_x: False
                    do_scroll_y: True
                    scroll_y: dp(10)
                    scroll_type: ['bars']
                    canvas.before:
                        Color:
                            rgba: 1, 0, 0, 1  # Red color for the border
                        Line:
                            rectangle: self.x, self.y, self.width, self.height
                            width: 1
                    Label:
                        id: song_info
                        height: dp(130)
                        size_hint: None, None
                        size: self.parent.width, dp(135)
                        text_size: self.width, self.height
                        text: ""
                        valign: 'top'
                        halign: 'left'
                        markup: True
                        canvas.before:
                            Color:
                                rgba: 0, 0, 0, 1
                            Line:
                                rectangle: self.x, self.y, self.width, self.height
                                width: 1
            AnchorLayout:
                anchor_x: 'center'  # Aligns children to the left
                anchor_y: 'top'
                BoxLayout:
                    # id: account_management
                    # orientation: 'vertical'
                    # size_hint_x: None
                    # width: self.minimum_size[0]
                    # spacing: dp(5)
                    # Button:
                        # text: 'Edit Account Info'
                        # size_hint: None, None
                        # size: dp(150), dp(30)
                        # background_color:[0,1,0,1]
                        # on_press:
                            # root.parent.parent.parent.parent.transition.direction = 'up'
                            # root.parent.parent.parent.parent.current = 'add_account_info_page'
                    # Button:
                        # text: 'Change Password'
                        # size_hint: None, None
                        # size: dp(150), dp(30)
                        # background_color:[0,1,0,1]
                        # on_press:
                            # root.parent.parent.parent.parent.transition.direction = 'up'
                            # root.parent.parent.parent.parent.current = 'change_password_page'
                    BoxLayout:
                        id: blank_space
                        orientation: 'vertical'
    BoxLayout:
        id: error_window
        size_hint: None, None
        size: self.minimum_size[0], dp(40)
        pos: -self.minimum_size[0], dp(350)
        opacity: 0
        padding: dp(10)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [5, 5, 5, 5]
        Label:
            id: window_message
            text: ''
            color: (0, 0, 0, 1)
            size_hint: None, None
            size: self.texture_size[0], dp(20)
            center: self.parent.center
    HoverableButton:
        size_hint: (None, None)
        size: dp(150), dp(30)
        text: 'Leave Session'
        offset: 0, -50
        pos_hint: {'x': 0.01, 'y': 0.01}
        background_color:[0,1,0,1]
        on_press:
            root.manager.transition.direction = 'up'
            root.submit()
""")

    # Spotivibe().run()

    sv = Spotivibe()
    if __name__ == '__main__':
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        sv.run()
    sv.check_user_session()
