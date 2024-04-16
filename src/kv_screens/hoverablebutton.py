from kivy.core.window import Window
from kivy.uix.button import Button

class HoverableButton(Button):
    def __init__(self, offset=(0, 0), **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)
        self.offset = offset

    def on_mouseover(self, window, pos):
        print(*pos)
        print(pos)
        adjusted_pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        if self.collide_point(*adjusted_pos):
            self.background_color = (0, 0.5, 0, 1)
        else:
            self.background_color = (0, 1, 0, 1)


