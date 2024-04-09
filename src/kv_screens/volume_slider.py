from kivy.uix.slider import Slider


class VolumeSlider(Slider):
    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        self.step = 1
        self.min = 0
        self.max = 100
        self.id = "volume_slider"
        super(VolumeSlider, self).__init__(**kwargs)

    def on_release(self):
        pass

    def on_touch_up(self, touch):
        super(VolumeSlider, self).on_touch_up(touch)
        if touch.grab_current == self:
            self.dispatch('on_release')
            return True
