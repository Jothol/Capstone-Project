from kivy.core.window import Window
from kivy.uix.button import Button

# Subclass of a button to define mouse hover functionality

class HoverableButton(Button):
    def __init__(self, offset=(0, 0), transition_color="green", **kwargs):
        super().__init__(**kwargs)
        # Bind window to the mouseover on position event
        Window.bind(mouse_pos=self.on_mouseover)
        # offset is used to adjust for different window pos than
        self.offset = offset
        # transition color is used to pick between green or grey buttons
        self.transition_color = transition_color

    def on_mouseover(self, window, pos):
        # Add offset to the mouse position
        adjusted_pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])

        if self.collide_point(*adjusted_pos):
            # If mouse is on button change the color
            if self.transition_color == "green":
                self.background_color = (0, 0.5, 0, 1)
            else:
                self.background_color = (0.3, 0.3, 0.3, 1)
        else:
            # When mouse is off button return to default color
            if self.transition_color == "green":
                self.background_color = (0, 1, 0, 1)
            else:
                self.background_color = (0.1, 0.1, 0.1, 1)


