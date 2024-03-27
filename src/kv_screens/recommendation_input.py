from kivy.uix.screenmanager import Screen


class RecommendationInputScreen(Screen):

    def submit(self, track):
        self.parent.ids.recInput = track
        print(self.parent.ids.recInput)
        self.parent.current = "recommendation_page"
