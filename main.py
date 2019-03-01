# -*- coding: utf-8 -*-
import telebot
import requests
from bs4 import BeautifulSoup as bs
from telebot import types
import urllib2

bot = telebot.TeleBot("726058560:AAEcAOI5010UEOx3Xz4waWXpG7sw0BrYwag")

# bot.send_message('686197998','Hello!')


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

        data = urllib2.urlopen(today)

        bot.send_document(message.chat.id, data, None, todayText)
        data = urllib2.urlopen(tomorrow)

        bot.send_document(message.chat.id, data, None, tomorrowText)
        # bot.send_message(message.chat.id, tomorrow)

    elif message.text == 'Расписание'.decode('utf-8'):

        n = 0
        for sch in schedule:
            bot.send_message(message.chat.id, schedule[n], None, scheduleText[n])
            n += 1

    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Замены')
    itembtn2 = types.KeyboardButton('Расписание')
    #  itembtn3 = types.KeyboardButton('3')
    # markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Выбери:", reply_markup=markup)
    print message.text


bot.polling(none_stop=True)
