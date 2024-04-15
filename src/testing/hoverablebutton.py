from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.app import App

class HoverableButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos):
        if self.collide_point(*pos):
            self.background_color = (0, 0, 1, 1)
        else:
            self.background_color = (0, 1, 0, 1)

class HoverApp(App):
    def build(self):
        return HoverableButton(text='Hover Me', size_hint=(None, None), size=(200, 50))

if __name__ == '__main__':
    HoverApp().run()