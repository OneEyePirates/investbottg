import time
import telebot
import sqlite3
import requests
import datetime
from coinbase.wallet.client import Client

import config

from etc import functions 
from classes.pay import qiwi
from classes.database import DataBase
from etc.adminka.text import messages as admin_messages




    


def addresses():
    addresses = []

    con = sqlite3.connect(config.PATH_2_BD)
    cursor = con.cursor()

    sql = "SELECT id, chat_id FROM Users ORDER BY last_use DESC"
    cursor.execute(sql)

    for id, chat_id in cursor.fetchall():
        sql = "SELECT id, address_id FROM Addresses WHERE chat_id = {}".format(chat_id)
        cursor.execute(sql)
        res = cursor.fetchone()
        if res != None:
            addresses.append(res[1])
    con.close()
    return addresses



def user_balance(address_id, new_balance):
    con = sqlite3.connect(config.PATH_2_BD)
    cursor = con.cursor()

    sql = "SELECT chat_id, balance FROM Addresses WHERE address_id = '{}'".format(address_id)
    cursor.execute(sql)
    chat_id, balance = cursor.fetchone()

    balance += 0.00000001


    if new_balance > float(balance): # Если пополнение есть
        refill = new_balance - balance + 0.00000001
        refill_text = "{:.8f}".format(round(refill, 8))

        sql = "UPDATE Addresses SET balance = {} WHERE address_id = '{}'".format(new_balance, address_id)
        cursor.execute(sql) # Обновление балансе в бд с адресами
 
        sql = "SELECT id FROM Money_operation"
        cursor.execute(sql)
        try:
            id = len(cursor.fetchone())+1
        except:
            id = 1

        sql = "INSERT INTO Money_operation VALUES(?, ?, ?, ?, ?)" # Запись в операции
        values = (id, refill_text, chat_id, "refill", "refill")
        cursor.execute(sql, values)

        sql = "UPDATE Users SET balance = balance + {} WHERE chat_id = {}".format(refill_text, chat_id) # Обновление баланса юзера
        cursor.execute(sql)


        config.bot.send_message(config.ADMINS_ID[0], "юзер <code>{}</code> пополнение баланс на {} btc".format(chat_id, refill_text), parse_mode="HTML")
        config.bot.send_message(chat_id, "🔥 Ваш баланс пополнен на {} BTC".format(refill_text))

    con.commit()
    con.close()







def main():
    client = Client(config.API_KEY, config.PRIVATE_KEY)
    account_id = client.get_primary_account()["id"]

    addresses_list = addresses()

    for address_id in addresses_list:
        transactions = client.get_address_transactions(account_id, address_id)["data"]
    

        if len(transactions) > 0:
            balance = 0
            for transaction in transactions:
                sum = float(transaction["amount"]["amount"])


                status = transaction["status"]
                hash = transaction["network"]["hash"]

                if status == "completed":
                    balance += sum

                elif 3 >= config.need_confirmations:
                    url = "https://api.blockcypher.com/v1/btc/main/txs/{}".format(hash)
                    r = requests.get(url)

                    try:
                        confirmations = int(r.json()["confirmations"])

                        if config.need_confirmations <= confirmations:
                            balance += sum

                    except:
                        pass


            user_balance(address_id, balance)



def check_qiwies():
    for qiwi_data in functions.get_qiwies():

        phone = qiwi_data["phone"]
        token = qiwi_data["token"]

        
        wallet = qiwi.QApi(num=phone, token=token)

        if qiwi_data["time_stamp"] < time.time() - 60 * 10:
        
            if False == wallet.check_valid_account(config.test_send_phone, 1):
                mes = admin_messages.add_qiwi_not_valid_two_step_message(phone, token)

                admin_chat_id = config.ADMINS_ID[0]

                try:
                    config.bot.send_message(admin_chat_id, mes, parse_mode="HTML")
                except:
                    pass


                DB = DataBase()
                DB.del_qiwi(phone)
                DB.close()

            else:
                now_balance = wallet.balance()


                if qiwi_data["balance"] != now_balance:
                    DB = DataBase()
                    DB.update_qiwi("balance", phone, now_balance)
                    DB.update_qiwi("time_stamp", phone, round(time.time()))
                    DB.close()


            

















