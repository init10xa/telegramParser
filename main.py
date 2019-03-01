# -*- coding: utf-8 -*-
import telebot
import requests
import re
from bs4 import BeautifulSoup as bs
from telebot import types
import urllib2

bot = telebot.TeleBot("SECRET")



#####PARSE#####

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

base_url = 'http://mcb.by/studentu/dnevnoje-otdelenije/raspisanie-zanyatiy'

tomorrow = None
today = None
todayText = None
tomorrowText = None
schedule = [0] * 10
scheduleText = [0] * 15
session = requests.session()
request = session.get(base_url, headers=headers)
if request.status_code == 200:
    soup = bs(request.content, 'html.parser')
    p = soup.find_all('p')
    i = 0
    n = 0
    for ps in p:
        strong = ps.find('strong')
        if strong is not None:
            text = ps.find('a').text
            print i
            if i == 0:
                today = ps.find('a')['href']
                todayText = text
                i += 1
            elif i == 1:
                tomorrowText = text
                tomorrow = ps.find('a')['href']
                i += 2

            elif i >= 3:
                print 'tfx'
                schedule[n] = ps.find('a')['href']
                scheduleText[n] = text
                i += 1
                n += 1






else:
    print 'lol'


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == 'Замены'.decode('utf-8'):
        sendfile(today, message, None)
        sendfile(tomorrow, message, None)

        # bot.send_message(message.chat.id, tomorrow)

    elif message.text == 'Расписание'.decode('utf-8'):

        n = 0
        for sch in schedule:
            sendfile(schedule[n], message, scheduleText[n])
            # bot.send_message(message.chat.id, schedule[n], None, scheduleText[n])
            n += 1

    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Замены')
    itembtn2 = types.KeyboardButton('Расписание')
    #  itembtn3 = types.KeyboardButton('3')
    # markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Выбери:", reply_markup=markup)
    print message.text


def sendfile(day, message, text):
    regData = re.findall("id.+", day)
    print 'https://drive.google.com/uc?authuser=0&' + regData[0] + '&export=download'
    data = urllib2.urlopen('https://drive.google.com/uc?authuser=0&' + regData[0] + '&export=download')
    datatowrite = data.read()
    with open('/Users/vanec/Downloads/schedule.pdf', 'wb') as f:
        f.write(datatowrite)

    if day == tomorrow:
        bot.send_document(message.chat.id, open('/Users/vanec/Downloads/schedule.pdf', 'rb'), None, tomorrowText)
    elif day == today:
        bot.send_document(message.chat.id, open('/Users/vanec/Downloads/schedule.pdf', 'rb'), None, todayText)
    else:
        bot.send_document(message.chat.id, open('/Users/vanec/Downloads/schedule.pdf', 'rb'), None, text)


bot.polling(none_stop=True)
