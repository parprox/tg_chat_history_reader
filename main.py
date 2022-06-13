from os import path
import json
import hashlib

from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

# from data_parcing_functions import get_chat_data
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


def get_chat_data(path):
    try:
        with open(path, encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        post_datetimes = soup.find_all("div", class_="pull_right date details")
        post_texts = soup.find_all("div", class_="text")

        for post_text in post_texts:
            inside_soup = post_text
            for br in inside_soup.find_all('br'):
                br.replace_with("\n")

        data_list = []

        # for index in range(0, len(post_datetimes)):
        #     print(post_texts[index+1])

        if len(post_texts) - len(post_datetimes) == 1:
            for index in range(0, len(post_datetimes)):
                data_list.append({'post_datetime': post_datetimes[index]['title'], 'post_text': post_texts[index+1].text})
        elif len(post_datetimes) - len(post_texts) == 1:
            for index in range(0, len(post_texts)):
                data_list.append({'post_datetime': post_datetimes[index+1]['title'], 'post_text': post_texts[index].text})
        elif len(post_texts) - len(post_datetimes) == 0:
            for index in range(0, len(post_texts)):
                data_list.append({'post_datetime': post_datetimes[index]['title'], 'post_text': post_texts[index].text})
        else:
            for index in range(0, len(post_texts)):
                data_list.append({'post_datetime': "Дата и время не были корректно определены", 'post_text': post_texts[index].text})

        return data_list

    except Exception:
        return False


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
