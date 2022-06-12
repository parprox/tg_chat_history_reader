from bs4 import BeautifulSoup

path = f"ChatOpenSource/messages.html"

def get_chat_data(path):
    with open(path, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    post_datetimes = soup.find_all("div", class_="pull_right date details")
    post_texts = soup.find_all("div", class_="text")

    data_list = []

    for index in range(0, len(post_datetimes)):
        data_list.append({'post_datetime': post_datetimes[index]['title'], 'post_text': post_texts[index+1].text})

    return data_list

if __name__=="__main__":
    print(get_chat_data(path))