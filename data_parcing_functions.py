from bs4 import BeautifulSoup

path = f"ChatAliExpressHacker/messages.html"

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

if __name__=="__main__":
    print(get_chat_data(path))
