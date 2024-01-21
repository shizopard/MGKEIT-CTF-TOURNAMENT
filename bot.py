import telebot
from telebot import types
import json
import random
import sys
import os

def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    

def check_and_add_user(user_id):
    try:
        with open('msg.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    if user_id not in data:
        data.append(user_id)
        with open('msg.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

def send_message_to_all_users(text):
    try:
        with open('msg.json', 'r', encoding='utf-8') as file:
            user_ids = json.load(file)

        for user_id in user_ids:
            try:
                bot.send_message(user_id, text)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {str(e)}")

    except FileNotFoundError:
        print("Файл msg.json не найден")


ALLOWED_USERS = ["5688214328", "456"]
#########################################
RESTRICTIONS_ENABLED = False # МЕНЯТЬ ЭТО 
#########################################

def is_allowed(user_id):
    if RESTRICTIONS_ENABLED and user_id not in ALLOWED_USERS:
        return False
    return True

# PATCHS
commands_file = 'commands.json'
users_file = 'users.json'
users_data = load_users()


bot = telebot.TeleBot('token here')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    users_data = load_users()
    user_id = str(message.from_user.id)

    if is_allowed(user_id):
        pass
    else:
        bot.send_message(message.chat.id, "Вам запрещено использовать бота.")
        return 

    global commands_message
    users = load_users()
    users_data = load_users()
    user_id = str(message.from_user.id)
    user_id = str(message.from_user.id)

    # мэйн команда бота
    if message.text == "/start":
        check_and_add_user(user_id)        
        if user_id in users:
            markup = types.InlineKeyboardMarkup()
            top_commands = types.InlineKeyboardButton('Рейтинг команд', callback_data='top_list')
            my_command = types.InlineKeyboardButton('Моя команда', callback_data='my_command')
            tasks = types.InlineKeyboardButton('Задания', callback_data='tasks')
            markup.add(top_commands, my_command)
            markup.add(tasks)
            bot.send_message(message.chat.id, "Это меню бота, здесь можно просмотреть информацию об игре\nНо сейчас есть дело поважнее - скорее переходи к заданиям!", reply_markup=markup)
        else:
            photo_path = 'preview.png'
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            markup = types.InlineKeyboardMarkup()
            next_step_button = types.InlineKeyboardButton('Продолжай', callback_data='next_step_button')
            markup.add(next_step_button)
            bot.send_message(message.chat.id, """
Привет! В систему нашего колледжа проник вирус, который захватил главный компьютер.
Твоя задача - узнать о происхождении вируса, как он попал в систему, кто за этим стоит и какой вред он может нанести.
Бот создан на базе нашего колледжа для защиты от посторонних программ, но вирус оказался сильнее, и тебе необходимо помочь нам одолеть вирус.

Код для доступа к главному компьютеру, где базируется вирус, зашифрован в ответах на задачи.
Далее расскажу подробнее о турнире.
""", reply_markup=markup)
            
    elif message.text == "/al":
        markup = types.InlineKeyboardMarkup()
        alist = types.InlineKeyboardButton('Команды', callback_data='atop_list')
        markup.add(alist) 
        bot.send_message(message.chat.id, 'Панель управления', reply_markup=markup)
    elif message.text == "/shzpard_luchiy_proger":
        RESTRICTIONS_ENABLED = True
        send_message_to_all_users("🔔 Участники!\n3 команды-финалиста были набраны, сбор в библиотеке.")
        sys.exit()
    elif message.text == "/shzpard_top_proger":
        RESTRICTIONS_ENABLED = False
        bot.send_message(message.chat.id, "Ограничения отключены")

    elif message.text.startswith("/send"):
        if message.from_user.id == 5688214328:
            if user_id in ALLOWED_USERS:
                text_to_send = message.text.replace("/send", "").strip()
                send_message_to_all_users(text_to_send)
                bot.send_message(message.chat.id, f"Сообщение '{text_to_send}' отправлено всем пользователям.")
            else:
                bot.send_message(message.chat.id, "У вас нет прав на использование этой команды.")


    elif message.text == "/admin":
        user_id = message.from_user.id
        user_status = get_user_status(user_id)
        if user_status == 1:
            markup = types.InlineKeyboardMarkup()
            add_command = types.InlineKeyboardButton('Добавить команду', callback_data='add_command')
            give_balls = types.InlineKeyboardButton('Выдать подсказки', callback_data='give_balls')
            markup.add(add_command, give_balls)
            bot.send_message(message.chat.id, "Навигация администратора:\n- Добавить команду - добавляет новую команду\n- Выдать баллы - выдает баллы команде по ID", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
# переход к объяснению о турнире
    if call.data == 'next_step_button':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        markup = types.InlineKeyboardMarkup()
        start_step_button = types.InlineKeyboardButton('Начнем!', callback_data='start_step_button')
        markup.add(start_step_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=""" 
В ходе турнира тебе предстоит решать задачи. Запоминайте части шифра, которые вы узнаете при вводе правильного ответа. В конце, они будут необходимы для доступа к главному компьютеру.
                              
""", reply_markup=markup)

 # выбор игры в одиночку или присоедиинение к команде       
    elif call.data == 'start_step_button':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        markup = types.InlineKeyboardMarkup()
        singleplay = types.InlineKeyboardButton('Создать команду', callback_data='singleplay')
        connect_to_command = types.InlineKeyboardButton('Присоединиться к команде', callback_data='connect_to_command')
        markup.add(singleplay)
        markup.add(connect_to_command)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Создай свою команду или присоединись к существующей", reply_markup=markup)

# игра в одиночку, переход к созданию команды
    elif call.data == 'singleplay':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Смелое решение! Придумай название для своей команды, оно будет отображаться в списке всех команд")
        bot.register_next_step_handler(call.message, process_user_command)

# подключение к команде  
    elif call.data == 'connect_to_command':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите код подключения к команде. Его можно запросить у капитана")
        bot.register_next_step_handler(call.message, connect_user_to_command)

# возвращение к меню

    elif call.data == 'gostart':
        user_id = str(call.from_user.id)
        if RESTRICTIONS_ENABLED == True:
            if not is_allowed(user_id):
                return
        markup = types.InlineKeyboardMarkup()
        top_commands = types.InlineKeyboardButton('Рейтинг команд', callback_data='top_list')
        my_command = types.InlineKeyboardButton('Моя команда', callback_data='my_command')
        tasks = types.InlineKeyboardButton('Задания', callback_data='tasks')
        markup.add(top_commands, my_command)
        markup.add(tasks)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Это меню бота, здесь можно просмотреть информацию об игре\nНо сейчас есть дело поважнее - скорее переходи к заданиям!", reply_markup=markup)

    # инфа о команде
    
    elif call.data == 'my_command':
        user_id = str(call.from_user.id)
        user_data = load_users()

        if user_id in user_data:
            user_command_id = user_data[user_id]['user_command_id']
            command_data = load_commands()

            if str(user_command_id) in command_data:
                current_task_number = command_data[str(user_command_id)]['now_task']
                if current_task_number == 6:
                    current_task_number = str("Финал")
                command_name = command_data[str(user_command_id)]['command_name']
                ball_value = command_data[str(user_command_id)]['ball']
                captain_username = command_data[str(user_command_id)]['captain_username']
                markup = types.InlineKeyboardMarkup()
                back = types.InlineKeyboardButton('Назад', callback_data='gostart')
                markup.add(back)
                text = f"Информация о вашей команде:\n" \
                    f"ID: {user_command_id}\n" \
                    f"Название команды: {command_name}\n" \
                    f"Текущее задание: {current_task_number}\n" \
                    f"Капитан команды: @{captain_username}"

                bot.edit_message_text(chat_id=call.message.chat.id, 
                                    message_id=call.message.message_id,
                                    text=text, reply_markup=markup)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Ваша команда не найдена")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Вы не найдены в базе данных")
             
# просмотр списка заданий
    elif call.data == 'tasks':
        try:
            with open('users.json', 'r', encoding='utf-8') as users_file:
                users_data = json.load(users_file)
                command_data = load_commands()
                user_id = str(call.from_user.id)
                if user_id in users_data:
                    user_data = load_users()
                    user_command_id = user_data[user_id]['user_command_id']
                    current_task_number = command_data[str(user_command_id)]['now_task']
                    task_number = int(current_task_number)
                    
                    with open('tasks.json', 'r', encoding='utf-8') as tasks_file:
                        tasks_data = json.load(tasks_file)
                        current_task = tasks_data.get('task', {}).get(str(task_number))

                        if current_task:
                            task_name = current_task.get('name', 'Нет названия задачи')
                            task_fine = current_task.get('fine', 'У вас нет задачи')
                            process_task(call, task_name, task_fine)
                        else:
                            markup = types.InlineKeyboardMarkup()
                            goback = types.InlineKeyboardButton('Назад', callback_data='gostart')
                            markup.add(goback)
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="У вас нет заданий", reply_markup=markup)
                else:
                    bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text="Вы не найдены в базе данных"
                    )

        except FileNotFoundError:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Файл заданий не найден"
            )

# отправка ответа на задание (переход к функции)
    elif call.data == 'give_answer':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        markup = types.InlineKeyboardMarkup()
        back_to_tasks = types.InlineKeyboardButton('К заданиям', callback_data='tasks')
        markup.add(back_to_tasks)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправьте ответ на задание", reply_markup=markup)
        bot.register_next_step_handler(call.message, get_user_answer)

# подсазка к заданию
    elif call.data == 'helpme':
        if is_allowed(user_id):
            pass
        else:
            return 
        user_id = str(call.from_user.id)
        user_data = load_users()
        if user_id in user_data:
            current_task_number = user_data[user_id]['now_task']
            try:
                with open('tasks.json', 'r', encoding='utf-8') as tasks_file:
                    tasks_data = json.load(tasks_file)
                    current_task = tasks_data['task'].get(str(current_task_number))
                    if current_task:
                        task_tip = current_task.get('tip')
                        markup = types.InlineKeyboardMarkup()
                        markup = types.InlineKeyboardMarkup()
                        give_answer = types.InlineKeyboardButton('Отправить ответ', callback_data='give_answer')
                        goback = types.InlineKeyboardButton('Назад', callback_data='gostart')
                        markup.add(give_answer)
                        markup.add(goback)
                        user_data = load_users()
                        user_command_id = user_data[user_id]['user_command_id']
                        command_data = load_commands()
                        now_balls = command_data[str(user_command_id)]['ball']
                        print(now_balls)
                        command_data[str(user_command_id)]['ball'] -= 1
                        save_commands(command_data)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ Подсказка: {task_tip}", reply_markup=markup)
                        
                    else:
                        bot.send_message(call.message.chat.id, "У вас нет текущего задания")
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, "Файл заданий не найден")
        else: 
            bot.send_message(call.message.chat.id, "Вы не найдены в базе данных")

# топ команд
    elif call.data == 'top_list':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        all_commands_text = list_all_commands()
        markup = types.InlineKeyboardMarkup()
        goback = types.InlineKeyboardButton('Назад', callback_data='gostart')
        markup.add(goback)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=all_commands_text, reply_markup=markup)

    elif call.data == 'amenu':
        markup = types.InlineKeyboardMarkup()
        alist = types.InlineKeyboardButton('Команды', callback_data='atop_list')
        markup.add(alist)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Панель администратора", reply_markup=markup)
    elif call.data == 'atop_list':
        user_id = str(call.from_user.id)
        if is_allowed(user_id):
            pass
        else:
            return 
        all_commands_text = alist_all_commands()
        markup = types.InlineKeyboardMarkup()
        goback = types.InlineKeyboardButton('Назад', callback_data='amenu')
        markup.add(goback)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=all_commands_text, reply_markup=markup)

    elif call.data == 'top_commands':
        if is_allowed(user_id):
            pass
        else:
            return 
        try:
            all_commands_text = list_all_commands()
            markup = types.InlineKeyboardMarkup()
            give_answer = types.InlineKeyboardButton('Отправить ответ', callback_data='give_answer')
            goback = types.InlineKeyboardButton('Назад', callback_data='gostart')
            markup.add(give_answer)
            markup.add(goback)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Задание: {task_name}\n💲 Штраф за подсказку: -{task_fine}B\n✅ Подсказка получена", reply_markup=markup)
        except:
            markup = types.InlineKeyboardMarkup()
            goback = types.InlineKeyboardButton('Назад', callback_data='gostart')
            markup.add(goback)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Неизвестная ошибка (#4)", reply_markup=markup)

# Просмотр списка всех команд
        
def list_all_commands():
    commands_text = ""
    try:
        with open(commands_file, 'r', encoding='utf-8') as file:
            commands_data = json.load(file)
            for command_id, data in commands_data.items():
                user_command = data.get('command_name', 'Нет названия команды')
                now_task = data.get('now_task', 'Нет данных о задании')
                commands_text += f"Название: {user_command}\nТекущее задание: №{now_task}\n=======================\n"
    except FileNotFoundError:
        commands_text = "Файл с командами не найден"
    return commands_text

def alist_all_commands():
    commands_text = ""
    try:
        with open(commands_file, 'r', encoding='utf-8') as file:
            commands_data = json.load(file)
            for command_id, data in commands_data.items():
                user_command = data.get('command_name', 'Нет названия команды')
                command_captain = data.get('command_captain', 'Нет id капитана')
                captain_username = data.get('captain_username', 'Нет username капитана')      
                now_task = data.get('now_task', 'Нет данных о задании')
                users = data.get('users', 'Нет данных о команде')
                commands_text += f"Название: {user_command} [ID: {command_id}]\nТекущее задание: №{now_task}\nКапитан: @{captain_username} ID:({command_captain})\nУчастники:\n{users}\n=======================\n"
    except FileNotFoundError:
        commands_text = "Файл с командами не найден"
    return commands_text

def get_user_answer(message):
    user_id = str(message.from_user.id)
    tasks_file = "tasks.json"
    user_data = load_users()

    if user_id in user_data:
        user_command_id = user_data[user_id]['user_command_id']
        command_data = load_commands()

        if str(user_command_id) in command_data:
            current_task_number = command_data[str(user_command_id)]['now_task']

            try:
                with open(tasks_file, 'r', encoding='utf-8') as file:
                    tasks_data = json.load(file)
                    current_task = tasks_data['task'].get(str(current_task_number))

                    if current_task:
                        task_name = current_task.get('name')
                        correct_answer = current_task.get('answer')
                        next_step = current_task.get('tip')
                        task_hash = current_task.get('hash')
                        user_answer = message.text.strip()

                        if user_answer.lower() == correct_answer.lower():
                            markup = types.InlineKeyboardMarkup()
                            goback = types.InlineKeyboardButton('В меню', callback_data='gostart')
                            to_answer = types.InlineKeyboardButton('Отправить ответ', callback_data='give_answer')   
                            markup.add(goback, to_answer)
                            if current_task_number == 4:
                                bot.send_message(message.chat.id, "Найдите этого человека: 17-6-20-18-6-15-12-16 10-18-10-15-1 3-13-1-5-10-14-10-18-16-3-15-1")
                            bot.send_message(message.chat.id, f"#answer\n✅ Правильный ответ!\nЧасть шифра: {correct_answer}\n\nИспользуй хештег, чтобы найти все части шифра, которые у тебя есть в этом диалоге\n❗️ Сохраняйте текст задания/подсказку к нему, которая отправлена ниже. Получить ее повторно нельзя")
                            if current_task_number == 3:
                                photo_path = 'first.jpg'
                                with open(photo_path, 'rb') as photo:
                                    bot.send_photo(message.chat.id, photo)
                            elif current_task_number == 2:
                                photo_path = 'second.jpg'
                                with open(photo_path, 'rb') as photo:
                                    bot.send_photo(message.chat.id, photo)
                            if current_task_number != 5:
                                bot.send_message(message.chat.id, f"{next_step}", reply_markup=markup)
                            else:
                                bot.send_message(message.chat.id, f"Задания в боте закончились Скорее отправляйтесь в библиотеку к финальному заданию!")
                            command_data[str(user_command_id)]['now_task'] = current_task_number + 1
                            command_data[str(user_command_id)]['ball'] += 1
                            save_commands(command_data)
                            user_data[user_id]['now_task'] = current_task_number + 1
                            save_users(user_data)
                            notify_team(current_task_number, user_id, user_command_id)
                            
                        else:
                            markup = types.InlineKeyboardMarkup()
                            back_to_menu = types.InlineKeyboardButton('Назад', callback_data='tasks')
                            markup.add(back_to_menu)
                            bot.send_message(message.chat.id, "❌ Ответ неверный :(\nПопробуй еще раз!", reply_markup=markup)
                    else:
                        markup = types.InlineKeyboardMarkup()
                        back_to_menu = types.InlineKeyboardButton('Назад', callback_data='gostart')
                        markup.add(back_to_menu)
                        bot.send_message(message.chat.id, "Если все основные задачи выполнены, выполните финальную задачу в библиотеке.", reply_markup=markup)
            except FileNotFoundError:
                bot.send_message(message.chat.id, "Файл заданий не найден")
        else:
            bot.send_message(message.chat.id, "Ваша команда не найдена")
    else:
        bot.send_message(message.chat.id, "Вы не найдены в базе данных")




# Присоединиться к команде
        
def connect_user_to_command(message):
    global user_connect_to_command
    user_connect_to_command = message.text
    user_chat_id = message.chat.id
    command_id = message.text
    user_id = str(message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    back_to_menu = types.InlineKeyboardButton('К меню', callback_data='gostart')
    markup.add(back_to_menu)
    
    with open('commands.json', 'r') as commands_file:
        commands_data = json.load(commands_file)
        
    if command_id not in commands_data:
        markup = types.InlineKeyboardMarkup()
        gotoback = types.InlineKeyboardButton("Назад", callback_data="start_step_button")
        markup.add(gotoback)
        bot.send_message(message.chat.id, "Команды с таким ID не существует", reply_markup=markup)
        return
    
    bot.send_message(message.chat.id, f"Задание №1\nМолодые осинтеры, поднимитесь на 3 этаж в холл.\nПервое задание ждет вас!\nВашей задачей является найти QR-код с дополнительной информацией. Ответ на задание необходимо ввести в бота")
    bot.send_message(message.chat.id, f"Вы успешно присоединились к команде!\nID: {command_id}", reply_markup=markup)

    with open('users.json', 'r') as users_file:
        users_data = json.load(users_file)
        users_data[user_id] = {
            "username": message.from_user.username,
            "user_in_command": user_connect_to_command,
            "isCaptain": False,
            "user_command_id": int(command_id),
            "now_task": 1,
            "chat_id": user_chat_id
        }
    with open('users.json', 'w') as users_file:
        json.dump(users_data, users_file, indent=4)
    
    if command_id in commands_data:
        commands_data[command_id]["users"].append(int(user_id))
        with open('commands.json', 'w') as commands_file:
            json.dump(commands_data, commands_file, indent=4)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка при добавлении пользователя в команду.")


# Создание команды (соло игра)
        
def process_user_command(message):
    global user_command
    user_command = message.text
    command_id = random.randint(100, 999)
    user_id = message.from_user.id
    username = message.from_user.username
    markup = types.InlineKeyboardMarkup()
    gostart = types.InlineKeyboardButton('Начинаем!', callback_data='gostart')
    markup.add(gostart)
    bot.send_message(message.chat.id, f"✅ Команда успешно создана\nНазвание команды: {user_command}\nID команды: {command_id}")
    bot.send_message(message.chat.id, f"Задание №1\nМолодые осинтеры, поднимитесь на 3 этаж в холл.\nПервое задание ждет вас!\nВашей задачей является найти QR-код с дополнительной информацией. Ответ на задание необходимо ввести в бота")
    bot.send_message(message.chat.id, f"Начнем!", reply_markup=markup)
    save_command(command_id, user_command, user_id, username)


# Сохранение данных о новой команде
def load_commands():
    try:
        with open(commands_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_commands(commands):
    with open(commands_file, 'w', encoding='utf-8') as file:
        json.dump(commands, file, indent=4)

def save_command(command_id, user_command, user_id, username):
    try:
        with open(commands_file, 'r', encoding='utf-8') as file:
            commands_data = json.load(file)
    except FileNotFoundError:
        commands_data = {}

    commands_data[str(command_id)] = {
        'command_id': command_id,
        'command_name': user_command,
        'command_captain': user_id,
        'captain_username': username,
        'ball': 2,
        'status': 0,
        'now_task': 1,
        'users': [user_id]
    }

    with open(commands_file, 'w', encoding='utf-8') as file:
        json.dump(commands_data, file, indent=4)

    #################################################

    try: 
        with open(users_file, 'r', encoding='utf-8') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        users_data = {}
    
    users_data[int(user_id)] = {
        'username': username,
        'user_in_command': user_command,
        'isCaptain': True,
        'user_command_id': command_id,
        'now_task': 1,
        'chat_id': user_id
    }
    with open(users_file, 'w', encoding='utf-8') as file:
        json.dump(users_data, file, indent=4)

def get_task_answers():
    with open('tasks.json', 'r') as file:
        tasks_data = json.load(file)
        answers = []
        for task_id, task_info in tasks_data['task'].items():
            if 'answer' in task_info:
                answers.append(task_info['answer'])
        return answers
    
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file)

def get_user_status(user_id):
    with open('users.json', 'r') as file:
        users_data = json.load(file)
        user = users_data.get(str(user_id))
        if user:
            return user.get("status")
    return None

def process_task(call, task_name, task_fine):
    markup = types.InlineKeyboardMarkup()
    give_answer = types.InlineKeyboardButton('Отправить ответ', callback_data='give_answer')
    goback = types.InlineKeyboardButton('Назад', callback_data='gostart')
    markup.add(give_answer)
    markup.add(goback)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"{task_name}",
        reply_markup=markup
    )

def get_task_name(task_number):
    tasks_file = "tasks.json"

    try:
        with open(tasks_file, 'r', encoding='utf-8') as file:
            tasks_data = json.load(file)
            current_task = tasks_data['task'].get(str(task_number))
            if current_task:
                return current_task.get('name', 'Нет названия задания')
    except FileNotFoundError:
        return 'Ошибка: файл заданий не найден'

def notify_team(task_number, user_id, user_command_id):
    command_data = load_commands()

    if str(user_command_id) in command_data:
        command_users = command_data[str(user_command_id)]['users']

        for user in command_users:
            user_id_str = str(user)
            if user_id_str != str(user_id):  # Исключаем отправителя уведомления
                try:
                    user_chat_id = users_data[user_id_str]['chat_id']
                    print(f"кто-то решил задание ({user_chat_id})")
                except KeyError:
                    print(f"Ошибка: нет 'chat_id' для пользователя {user_id_str}")
    else:
        print("Ошибка: команда не найдена")
        
bot.polling(none_stop=True, interval=0)