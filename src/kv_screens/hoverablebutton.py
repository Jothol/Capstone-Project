from kivy.core.window import Window
from kivy.uix.button import Button

class HoverableButton(Button):
    def __init__(self, offset=(0, 0), transition_color="green", **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)
        self.offset = offset
        self.transition_color = transition_color

    def on_mouseover(self, window, pos):
        adjusted_pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        if self.collide_point(*adjusted_pos):
            if self.transition_color == "green":
                self.background_color = (0, 0.5, 0, 1)
            else:
                self.background_color = (0.3, 0.3, 0.3, 1)
        else:
            if self.transition_color == "green":
                self.background_color = (0, 1, 0, 1)
            else:
                self.background_color = (0.1, 0.1, 0.1, 1)


