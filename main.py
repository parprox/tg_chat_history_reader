from kivy.core.window import Window
from kivy.properties import ObjectProperty

from data_parcing_functions import get_chat_data

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

#Set the app size
Window.size = (500, 700)

#Прямое указание, какой файл дизайна использовать
Builder.load_file('tg_chat_history_reader.kv')

class MyLayout(Widget):
    chat_data = get_chat_data(f"ChatOpenSource/messages.html")
    def start_button_click(self):
        self.ids.post_datetime.text = f"Пост был опубликован: {self.chat_data[0].get('post_datetime')}"
        self.ids.post_text.text = f"{self.chat_data[0].get('post_text')}"
        self.ids.post_index.text = f"{0}"


class AwesomeApp(App):
    def build(self):
        # Window.clearcolor = (1, 1, 1, 1)
        return MyLayout()

if __name__=="__main__":
    AwesomeApp().run()