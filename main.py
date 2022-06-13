from os import path
import json
import hashlib

from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

from data_parcing_functions import get_chat_data
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder



#Set the app size
Window.size = (500, 700)

#Прямое указание, какой файл дизайна использовать
Builder.load_file('tg_chat_history_reader.kv')

def get_hash(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


class FileChooseWindow(Screen):

    tg_chat_file_path = StringProperty()

    def selected(self, filename):
        try:
            chat_data = get_chat_data(filename[0])
            if chat_data:
                self.ids.filechooser_label.text = f"Файл {filename[0]} можно прочитать"
                self.tg_chat_file = filename[0]
            else:
                self.ids.filechooser_label.text = f"Файл {filename[0]} нельзя прочитать"

        except Exception:
            pass

class ReaderWindow(Screen):
    post_index = NumericProperty(0)
    chat_data = ObjectProperty()
    file_hash = StringProperty()

    chat_dict = ObjectProperty(dict())
    if path.isfile("tg_reader_db.json"):
        with open("tg_reader_db.json", 'r', encoding='UTF-8') as file:
            chat_dict = json.load(file)

    def on_enter(self, *args):
        file_path = self.manager.get_screen('file_choose').tg_chat_file
        self.file_hash = get_hash(file_path)

        if not self.chat_dict:
            self.chat_dict.update({self.file_hash: self.post_index})
        else:
            self.post_index = self.chat_dict.get(get_hash(file_path))
            if self.post_index == None:
                self.post_index = 0

        self.chat_data = get_chat_data(file_path)
        self.ids.post_datetime.text = f"Пост был опубликован:\n {self.chat_data[self.post_index].get('post_datetime')}"
        self.ids.post_text.text = f"{self.chat_data[self.post_index].get('post_text')}"
        self.ids.post_index.text = f"{self.post_index}"

    def forward_button_click(self):
        try:
            self.post_index += 1
            self.ids.post_datetime.text = f"Пост был опубликован:\n {self.chat_data[self.post_index].get('post_datetime')}"
            self.ids.post_text.text = f"{self.chat_data[self.post_index].get('post_text')}"
            self.ids.post_index.text = f"{self.post_index}"

            self.chat_dict.update({self.file_hash: self.post_index})
            with open("tg_reader_db.json", "w", encoding="UTF-8") as file:
                json.dump(self.chat_dict, file, ensure_ascii=False, indent=4)


        except Exception:
            pass

    def back_button_click(self):
        try:
            self.post_index -= 1
            self.ids.post_datetime.text = f"Пост был опубликован:\n {self.chat_data[self.post_index].get('post_datetime')}"
            self.ids.post_text.text = f"{self.chat_data[self.post_index].get('post_text')}"
            self.ids.post_index.text = f"{self.post_index}"

            self.chat_dict.update({self.file_hash: self.post_index})
            with open("tg_reader_db.json", "w", encoding="UTF-8") as file:
                json.dump(self.chat_dict, file, ensure_ascii=False, indent=4)
        except Exception:
            pass

sm = ScreenManager()
sm.add_widget(FileChooseWindow(name='file_choose'))
sm.add_widget(ReaderWindow(name='reader'))


class AwesomeApp(App):

    def build(self):
        # Window.clearcolor = (1, 1, 1, 1)
        return sm

if __name__=="__main__":
    AwesomeApp().run()
