import kivy
kivy.require('2.3.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class LoginScreen(Widget):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def check_status(self):
        #print('button state is: {state}'.format(state=btn.state))
        print('username input text is: {txt}'.format(txt=self.username.text))
        print('password input text is: {txt}'.format(txt=self.password.text))

class SpotiVibe(App):
    def build(self):
        return LoginScreen()
    
if __name__ == '__main__':
    Builder.load_file('./src/kv_style/kivytesting.kv')
    SpotiVibe().run()