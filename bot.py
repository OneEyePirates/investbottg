import time
import telebot

# Мои библы
import config # Конфиг

# Библы из папок
import classes.shelve as shelve # Работа с временным хранилищем
import etc.messages as messages # Сообщения
import etc.functions as functions # Дополнительные функции
from classes.database import DataBase
from classes.pay import bitcoin, qiwi

bot = config.bot

def ifsost(message, sost):
    chat_id = message.chat.id
    message_text = message.text

    if sost == 1: # Когда юзер вводит баланс
        address = message.text
        if functions.check_address(address) == True:
            balance = functions.user_balance(chat_id) # Получение баланса юзера

            mes = messages.sum_removal(balance)
            key = telebot.types.InlineKeyboardMarkup() 
            b1 = telebot.types.InlineKeyboardButton(
                                    text="❌ Отмена", 
                                    callback_data="Кошелек")
            key.add(b1)
            SH = shelve.Temp(chat_id)
            SH.write_btc_address( address)
            SH.write_sost(2)
            SH.close()
       
        else:
            key = functions.close_key("⬅️ Назад")
            mes = messages.if_nevalid_address()
           
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")




    elif sost == 2: # Когда юзер вводит баланс
        key = telebot.types.InlineKeyboardMarkup() 
        b1 = telebot.types.InlineKeyboardButton(
                                    text="🆗 Отправить", 
                                    callback_data="Подтверждаю вывод")
        b2 = telebot.types.InlineKeyboardButton(
                                    text="⬅️ Назад", 
                                    callback_data="Кошелек")
        
        if functions.isdigit(message.text) == True:
            sum = round(float(message.text), 8) # Сумма перевода
            balance = functions.user_balance(chat_id) # Баланс юзера

            # Макс сумма на вывод
            max = float(functions.max_removal(balance, config.REMOVAL))
            if config.ON_REMOVAL <= sum <= max:
                SH = shelve.Temp(chat_id)
                SH.write_sum_in_btc(sum) # Запись суммы перевода
                address = SH.get_btc_address() # Получение адреса
                SH.write_sost(3) # Обновление состояния
                SH.close()
               
                key.add(b1)
                mes = messages.removal(address, sum, balance)

            else:
                mes = messages.sum_removal(balance)

        else: # Если в сообщение не цифра
            mes = "Сумма для вывода должна быть цифрой!\nВведите заново."

        key.add(b2)
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")



    elif sost == 4: # Когда хочет перевести деньги другому юзеру
        print(2)
        BD = DataBase()
        if functions.isdigit(message_text) == True: # Сообщения цифра ?
            payee_chat_id = message_text

            profile = BD.profile(payee_chat_id) # Профиль получателя
            if profile["status"] == "registered": # Если получатель зареган
                balance = BD.profile(chat_id)["profile"]["balance"]
                mes = messages.when_sum_transfer(balance)
                key = functions.close_key("Отменить перевод")

                SH = shelve.Temp(chat_id)
                SH.write_btc_address(payee_chat_id) # Запись адреса
                SH.write_sost(5) # Обновление состояния
                SH.close()

            elif profile["status"] == "not_registered": # Если не зареган
                mes = "Пользователя с таким chat_id не обнаружен"
                key = functions.close_key("Закрыть")


        elif message_text[0] == "@": # Если юзернейм
            payee_username = message_text[1:]

            profile = BD.profile(payee_username, search_by="username")

            if profile["status"] == "registered":
                balance = BD.profile(chat_id)["profile"]["balance"]
                mes = messages.when_sum_transfer(balance)
            
                payee_chat_id = profile["profile"]["chat_id"]

                SH = shelve.Temp(chat_id)
                SH.write_btc_address(payee_chat_id) # Запись адреса
                SH.write_sost(5) # Обновление состояния
                SH.close()

            elif profile["status"] == "not_registered":
                mes = messages.when_not_username()

        else:
            mes = messages.when_money_transfer()


        BD.close()
        key = functions.close_key("❌ Отмена")
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")

    elif sost == 5:
        key = telebot.types.InlineKeyboardMarkup() 
        b1 = telebot.types.InlineKeyboardButton(
                                    text="🆗 Перевести", 
                                    callback_data="Подтверждаю перевод")
        b2 = telebot.types.InlineKeyboardButton(
                                    text="⬅️ Назад", 
                                    callback_data="Кошелек")
        if functions.isdigit(message_text) == True:
            sum = float(functions.round(message.text)) # Сумма перевода
            balance = float(functions.user_balance(chat_id)) # Баланс юзера

            if 0 < sum <= balance:
                SH = shelve.Temp(chat_id)
                SH.write_sum_in_btc(sum) # Запись суммы перевода
                payee_chat_id = SH.get_btc_address() # id получателя
                SH.write_sost(6) # Обновление состояния
                SH.close()

                key.add(b1)
                mes = messages.transfer(payee_chat_id, sum, balance)

            else:
                mes = messages.when_sum_transfer(balance)

        else: # Если в сообщение не цифра
            mes = "Сумма для вывода должна быть цифрой!\nВведите заново."

        key.add(b2)
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")




    elif sost == 7:
        balance = float(functions.user_balance(chat_id))
        if functions.isdigit(message_text) == True: # Сообщения цифра ?
            sum = float(message_text)

            if 0 < sum <= balance:
                BD = DataBase()

                """Добавление ваучера в бд и получение кода"""
                code = BD.new_voucher(chat_id, sum)
                BD.close()
                link = functions.create_link("v_{}".format(code))

                mes = messages.when_create_voucher(code, sum, link)
                key = telebot.types.InlineKeyboardMarkup()
                b1 = telebot.types.InlineKeyboardButton(text="🆗", 
                                        callback_data="Ваучеры")
                key.add(b1)
                functions.update_sost(chat_id, 0)

            elif sum > balance or 0 >= sum:
                mes = "❌ Недостаточно средств для создания ваучера\n⚠️ Повторите ввод ⚠️"
                key = telebot.types.InlineKeyboardMarkup()
                b1 = telebot.types.InlineKeyboardButton(text="⬅️ Назад", 
                                        callback_data="Ваучеры")
                key.add(b1)
        else:
            mes = messages.create_voucher(balance)
            key = functions.close_key("❌ Отмена")

        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")





    elif sost == 8:
        voucher = message_text
        BD = DataBase()
        resp = BD.get_voucher(voucher)
        if resp["exist"] == False or resp["status"] == "activated":
            mes = messages.incorrect_voucher()
            bot.send_message(chat_id, mes)

        elif resp["exist"] == True and resp["status"] == "not_activated":
            resp = BD.activate_voucher(voucher, message.chat.id)
            creator_chat_id, sum = resp
            sum = functions.round(sum)

            """Отправка уведомы создателю ваучера"""
            mes = messages.your_voucher_acvtivate(sum)
            bot.send_message(creator_chat_id, mes, parse_mode="HTML")
            BD.new_referal(chat_id, creator_chat_id) # Запись в рефералы

            """Активировавшему"""
            mes = messages.when_btc_came(sum)
            bot.send_message(chat_id, mes, parse_mode="HTML")

        BD.close()

        functions.update_sost(chat_id, 0) # Апдейт состояния юзера







    # Ждём сумму покупки btc
    elif sost == 9:
        btc_price = bitcoin.Btc().price()
        # print(btc)
        if functions.isdigit(message_text):
            sum = float(message_text)
            balance_in_btc = functions.balance_for_exchange()
            balance_in_rub = balance_in_btc * btc_price

            """Если сумму скинули в рублях"""
            if 1 <= sum:
                if config.min_byu_btc <= sum <= balance_in_rub:
                    sum = int(round(sum))
                    mes = two_step_byu_btc(chat_id, sum, btc_price)
                    key = telebot.types.InlineKeyboardMarkup()
                    b1 = telebot.types.InlineKeyboardButton(
                                        "Далее ➡️", 
                                        callback_data="Продолжить")
                    b2 = telebot.types.InlineKeyboardButton(text="❌ Отмена", 
                                        callback_data="Закрыть")
                    b3 = telebot.types.InlineKeyboardButton(text="⬅️ Назад", 
                                        callback_data="Купить BTC")
                    key.add(b3, b1)
                    key.add(b2)

                else:
                    mes = messages.re_step_byu_btc(balance_in_btc)
                    key = functions.close_key("⬅️ Назад")
                    

            elif 1 > sum:
                min_in_btc = config.min_byu_btc / btc_price
                if min_in_btc <= sum <= balance_in_rub / btc_price:
                    key = telebot.types.InlineKeyboardMarkup()
                    b1 = telebot.types.InlineKeyboardButton(
                                        "Далее ➡️", 
                                        callback_data="Продолжить")
                    b2 = telebot.types.InlineKeyboardButton(text="❌ Отмена", 
                                        callback_data="Закрыть")
                    b3 = telebot.types.InlineKeyboardButton(text="⬅️ Назад", 
                                        callback_data="Купить BTC")
                    key.add(b3, b1)
                    key.add(b2)
                    mes = two_step_byu_btc(chat_id, sum, btc_price)

                    

                else:
                    #mes = messages.one_step_byu_btc(balance_in_btc)
                    mes = messages.re_step_byu_btc(balance_in_btc)
                    key = functions.close_key("⬅️ Назад")

        else:
            balance_in_btc = functions.balance_for_exchange()
            mes = messages.re_step_byu_btc(balance_in_btc)
            key = functions.close_key("⬅️ Назад")

        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")


    # Ждём адрес для отправки btc
    elif sost == 10:
        #if functions.check_address(message_text):
            chat_id = message.chat.id
            qiwi_data = functions.get_qiwies()[0]
            BD = DataBase()
            address = BD.get_btc_address(message.chat.id)
            BD.close()
            SH = shelve.Temp(chat_id)

            #address = message_text
            need_me = SH.get_need_me()
            need_send = SH.get_need_send()

            phone, token = qiwi_data["phone"], qiwi_data["token"]


            wallet = qiwi.QApi(num=phone, token=token)

            comment = wallet.gen_comment()
            pay_form = wallet.pay_form(need_me, comment)

            SH.write_qiwi_data("{}:{}".format(phone, token))
            SH.write_btc_address(address)
            SH.write_sost(11)
            SH.write_comment(comment)
            SH.close()

            key = telebot.types.InlineKeyboardMarkup() 
            b1 = telebot.types.InlineKeyboardButton("✔ Я оплатил",
                                            callback_data="Проверить оплату")
            b2 = telebot.types.InlineKeyboardButton("❌ Отмена",
                                            callback_data="Закрыть")
            b3 = telebot.types.InlineKeyboardButton("🌐 Оплатить в браузере",
                                            url=pay_form)
            key.add(b1, b3)
            key.add(b2)

            mes = messages.four_step_byu_btc(phone, comment, need_me, need_send, address)


        #else:
            #key = functions.close_key("❌ Отмена")
            #mes = messages.if_nevalid_address()

            bot.edit_message_text(mes, chat_id=message.chat.id, reply_markup=key,
                          message_id=message.message_id,
                          parse_mode="HTML")













    # Ждём сумму для продажи битков
    elif sost == 12:
        btc_price = bitcoin.Btc().price()
        if functions.isdigit(message_text):
            sum = float(message_text)
            qiwi_balance = functions.qiwi_balance()

            """Если сумму скинули в рублях"""
            if 1 <= sum:
                if config.min_sell_btc <= sum <= qiwi_balance:
                    sum = int(round(sum))
                    mes = two_step_sell_btc(chat_id, sum, btc_price)
                    key = telebot.types.InlineKeyboardMarkup()
                    b1 = telebot.types.InlineKeyboardButton(
                                        "Далее ➡️", 
                                        callback_data="Продолжить1")
                    b2 = telebot.types.InlineKeyboardButton(text="⬅️ Назад", 
                                        callback_data="Продать BTC")
                    b3 = telebot.types.InlineKeyboardButton(text="❌ Отмена", 
                                        callback_data="Закрыть")
                    key.add(b2, b1)
                    key.add(b3)

                else:
                    
                    #mes = messages.one_step_sell_btc(qiwi_balance)
                    mes = messages.re_step_sell_btc(qiwi_balance)
                    key = functions.close_key("⬅️ Назад")
                    
                    #bot.send_message(chat_id, mes, parse_mode="HTML")

            elif 1 > sum:
                min_in_btc = config.min_sell_btc / btc_price
                if min_in_btc <= sum <= qiwi_balance / btc_price:
                    key = telebot.types.InlineKeyboardMarkup()
                    b1 = telebot.types.InlineKeyboardButton(
                                        "Далее ➡️", 
                                        callback_data="Продолжить1")
                    b2 = telebot.types.InlineKeyboardButton(text="❌ Отмена", 
                                        callback_data="Закрыть")
                    b3 = telebot.types.InlineKeyboardButton(text="⬅️ Назад", 
                                        callback_data="Продать BTC")
                    key.add(b3, b1)
                    key.add(b2)
                    mes = two_step_sell_btc(chat_id, sum, btc_price)
                    

                else:
                    
                    #mes = messages.one_step_sell_btc(qiwi_balance)
                    mes = messages.re_step_sell_btc(qiwi_balance)
                    key = functions.close_key("⬅️ Назад")
                    
                    #bot.send_message(chat_id, mes, parse_mode="HTML")
                    #bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")

        else:
            qiwi_balance = functions.qiwi_balance()
            mes = messages.re_step_sell_btc(qiwi_balance)
            #mes = messages.one_step_sell_btc(qiwi_balance)
            key = functions.close_key("❌ Отмена")
            #bot.send_message(chat_id, mes, parse_mode="HTML")

        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")


    elif sost == 13:
        if functions.isdigit(message_text):
            SH = shelve.Temp(chat_id)

            number = functions.num_validator(message_text)
            need_me = SH.get_need_me()
            need_send = SH.get_need_send()


            SH.write_btc_address(number)
            SH.write_sost(14)
            SH.close()

            key = telebot.types.InlineKeyboardMarkup() 
            b1 = telebot.types.InlineKeyboardButton("🆗️ Оплатить",
                                            callback_data="Оплатить с баланса бота")
            b2 = telebot.types.InlineKeyboardButton("❌ Отмена", 
                                            callback_data="Закрыть")
            key.add(b1, b2)

            mes = messages.four_step_sell_btc(number, need_me, need_send)

            bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")






def two_step_sell_btc(chat_id, sum, btc_price):
    sum = float(sum)
    resp = functions.sum_with_comission(sum, config.commission_on_sell, "sell")
    need_me = resp["need_me"]
    need_send = resp["need_send"]

    SH = shelve.Temp(chat_id)
    SH.need_send(need_send)
    SH.need_me(need_me)
    SH.close()

    mes = messages.two_step_sell_btc(btc_price, need_me, need_send)
    return mes    

            
                





def two_step_byu_btc(chat_id, sum, btc_price):
    sum = float(sum)
    resp = functions.sum_with_comission(sum, config.commission_on_byu, "byu")
    need_me = int(resp["need_me"])
    need_send = resp["need_send"]

    SH = shelve.Temp(chat_id)
    SH.need_send(need_send)
    SH.need_me(need_me)
    SH.close()

    mes = messages.two_step_byu_btc(btc_price, need_me, need_send)
    return mes
