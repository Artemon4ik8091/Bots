import os
import json
import time
from datetime import datetime, timedelta
import telebot
import random

global USERS_BALANCE
TEA_PRICE = 0 # цена чашки чая
USERS_BALANCE = {} # баланс пользователей (user_id: [balance, last_time_teapot])
BUFFER = 0
ANSWER = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_NAME = 'data.json'
DB_PATH = os.path.join(BASE_DIR, BASE_NAME)
AD = 0
AD_TEXT = ""

# если базы данных нет, то создаем новую
if not os.path.exists(DB_PATH):
    with open(DB_PATH, 'w') as f:
        json.dump({}, f)

# загружаем базу данных
with open(DB_PATH, 'r') as f:
    USERS_BALANCE = json.load(f)

#Загружаем токен из базы
bot = telebot.TeleBot(USERS_BALANCE['token'])

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет, я бот для чаепитий! ' 
                                      'Чтобы выпить чашку чая напиши /tea. '
                                      'Для проверки баланса напиши /bal. Настоятельно рекомендую ввести /help или /help@TeapartyDr_bot. '
                                      #'Разраб: @avenger_Pearce Канал бота: @roflsTeaParty'
                                      )

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, 'Для того чтобы выпить чай пиши /tea, для баланса - /bal. '
                 'Если ты в группе то используй /tea@TeapartyDr_bot и /bal@TeapartyDr_bot.')

@bot.message_handler(commands=['tea'])
def tea_message(message):
    global USERS_BALANCE
    user_id = str(message.from_user.id)
    user_name = message.from_user.username

    if not user_id in USERS_BALANCE:
        USERS_BALANCE[user_id] = [0.0, '']

    # проверяем, можно ли выпить чай
    BUFFER = float(random.randint(0, 5))
    ANSWER = float(random.randint(1, 3))
    # блок рекламы
    AD = int(random.randint(1,5))
    if(AD == 1):
        AD_TEXT = "\n\nРаздаем подзалупный творог прадеда Наварро, заходите\nhttps://t.me/War_bb111"
    if(AD == 2):
        AD_TEXT = "\n\nЗдесь могла бы быть ваша реклама но я её или не добавил или вы не писали её"
    if(AD == 3):
        AD_TEXT = "\n\nИщешь топ обзоры на блогеров? Тебе сюда -> https://youtube.com/@kivvi_nomom\n TG -> @kivvi_nomom"
    if(AD == 4):
        AD_TEXT = ""
    if(AD == 5):
        AD_TEXT = "\n\nКто добавит меня в какой нибудь чат и пришлёт пруфы сюда -> @avenger_Pearce тот получит 10 литров чая на баланс)"
    #BUFFER = 0
    #if (BUFFER >= 1.0):
    TEA_PRICE = BUFFER / 10
    try:
        last_teapot_time = datetime.strptime(USERS_BALANCE[user_id][1], '%Y-%m-%d %H:%M:%S')        
        time_delta = datetime.now() - last_teapot_time
        if time_delta.seconds < 1800:
            bot.reply_to(message, f'Ты уже пил чай {time_delta.seconds//60} минут назад. \n'
                                              f'Чай будет готов через {(30 - time_delta.seconds//60)} минут. ☕️'+ AD_TEXT)
            return
    except:
        pass

    # обновляем баланс пользователя
    balance = USERS_BALANCE[user_id]
    print(balance)
    #if (TEA_PRICE >= 0.1):
    balance[0] += TEA_PRICE
    balance[1] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    USERS_BALANCE[user_id] = balance

    with open(DB_PATH, 'w') as f:
        json.dump(USERS_BALANCE, f) # записываем изменения в базу данных
    if (TEA_PRICE < 0.1):
        bot.reply_to(message, "Ты пролил свой чай :(")
    if (TEA_PRICE >= 0.5):
        if (ANSWER == 1):
            bot.reply_to(message, "Ты выпил поллитровую банку чая. Куда столько?" + AD_TEXT)
        elif (ANSWER == 2):
            bot.reply_to(message, "Ты как это сделал? + 0.5 литров" + AD_TEXT)
        elif (ANSWER == 3):
            bot.reply_to(message, "0.5 литров чая = 1000 очков спокойствия и мотивации" + AD_TEXT)
    if (TEA_PRICE < 0.5 and TEA_PRICE != 0):
        if (ANSWER == 1):
            bot.reply_to(message, f'Ты выпил чашку чая объёмом ' + str(TEA_PRICE) + 'л. ☕️\nСделал как любишь, присладил немного ^_^' + AD_TEXT)
        if (ANSWER == 2):
            bot.reply_to(message, f'Привет! Рад видеть тебя, вот твой чай, наслаждайся ^_^\nТы выпил чашку чая объёмом ' + str(TEA_PRICE) + 'л. ☕️' + AD_TEXT)
        if (ANSWER == 3):
            bot.reply_to(message, f'Ты выпил чашку чая объёмом ' + str(TEA_PRICE) + 'л. ☕️\nТвой чай, наслаждайся ^_^' + AD_TEXT)

@bot.message_handler(commands=['bal'])
def balance_message(message):
    user_id = str(message.from_user.id)

    # проверяем баланс пользователя
    user_balance = USERS_BALANCE[user_id][0]

    bot.reply_to(message, f'Твой баланс: {user_balance} литров. ☕️')

bot.polling(none_stop=True)
