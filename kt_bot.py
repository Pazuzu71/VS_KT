import requests
from bs4 import BeautifulSoup
import telebot
from config import token, admin_id, url
import time
from datetime import datetime

bot = telebot.TeleBot(token)


def check_KT():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    r = requests.get(url=url, headers=headers)
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    tables = soup.find_all('table', class_="tbl")
    table = tables[1].find('table', class_="nil")
    b = table.find_all('b')
    b = [x.text for x in b]
    print(f'{datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M")}', b[1] > b[3])
    return b[1] > b[3]


@bot.message_handler(commands=['start'])
def start(msg):
    while True:
        if check_KT():
            try:
                bot.send_message(admin_id, 'Алярм! Новая заявка на КТ!', reply_to_message_id=msg.id)
            except Exception as ex:
                bot.send_message(admin_id, 'Исключение обработано')
                bot.send_message(admin_id, 'Алярм! Новая заявка на КТ!', reply_to_message_id=msg.id)
        # else:
        #     bot.send_message(admin_id, 'Заявок на КТ нет!', reply_to_message_id=msg.id)
        time.sleep(300)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as ex:
            print('Exception', ex)
