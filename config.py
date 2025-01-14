﻿import telebot

# --------------------------Токены--------------------------
BOT_TOKEN = "" # Токен бота
bot = telebot.TeleBot(BOT_TOKEN)
need_confirmations = 1
test_send_phone = 0
# --------------------------Токены--------------------------


# --------------------------Ссылки--------------------------
FAQ = "https://telegra.ph/FAQ-06-11-4"  # Ссылка на faq
SUPPORT = "https://t.me/username"  # Ссылка на саппорта
CHANNEL = "https://t.me/joinchat/AAAAAFh5vRwl2UsIN2mvJw"  # Ссылка на канал
RULES = "https://telegra.ph/Soglashenie-na-ispolzovanie-servisa-CryptExRobot-08-24" # Польз.соглашение
# --------------------------Ссылки--------------------------


# ---------------------------Файлы--------------------------
PATH_2_BD = "etc\data\data_base.db"
PATH_2_LOG = "etc\data\log.txt"
PATH_2_SH = "etc\data\sh\sost.bd"
# ---------------------------Файлы--------------------------


# -------------------------Coinbase-------------------------
API_KEY = ""  # Апи ключ от биржи
PRIVATE_KEY = ""
# -------------------------Coinbase-------------------------


# ---------------------------Юзеры--------------------------
ADMINS_ID = [123456, 654321]
# ---------------------------Юзеры--------------------------


# #------------------------Commission------------------------
REMOVAL = 0.0002  # Комиссия на вывод btc	
# ------------------------Commission------------------------


# --------------------------Limits--------------------------
ON_REMOVAL = 0.001 # мин. вывод btc
# --------------------------Limits--------------------------


# ------------------------Об обменах------------------------
min_byu_btc = 50 # мин. покупка (руб)
min_sell_btc = 599 # мин. продажа

commission_on_byu = 8 # на покупку BTC %
commission_on_sell = -5 # на продажу %

REFERAL_INCOME = 10 # реф. %
