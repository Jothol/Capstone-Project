import kivy
from kivy.uix.screenmanager import Screen

kivy.require('2.3.0')

class ChangePassword(Screen):
    def submit(self, password, re_password):
        if password != re_password:
            self.ids.error_message.text = "Passwords do not match."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif password == "":
            self.ids.error_message.text = "Password cannot be blank."
            self.ids.error_message.color = [1, 0, 0, 1]
        elif password == self.parent.ids.username.get_password():
            self.ids.error_message.text = "Password must be new."
            self.ids.error_message.color = [1, 0, 0, 1]
        else:
            self.parent.ids.username.reset_password(password)
            self.parent.current = 'home_page'
