import json

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dotenv import load_dotenv
import os
import vk_massages as ms

load_dotenv()

token = os.getenv(key='ACCESS_TOKEN')
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)


# def get_user_response(vk_session, user_id, message):
#     vk_session.method('messages.send', {
#         'user_id': user_id,
#         'message': message,
#         'random_id': get_random_id()
#     })
#     for event in VkLongPoll(vk_session).listen():
#         if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#             return event.text


# def create_user_profile(user_id, vk_session):
#     user_info = {
#         "user_id": user_id,
#         "sex": user_id
#     }
#
#     questions = {
#         "first_name": "Как тебя зовут?",
#         "last_name": "Отлично! А какая у тебя фамилия?",
#         "age": "Прекрасно! Сколько тебе лет?",
#         "city": "Замечательный возраст , мы почти закончили! В каком городе ты живешь?",
#         "about_me": "Прекрасно! Можешь кратко рассказать о своей жизни",
#     }
#
#     for key, question in questions.items():
#         user_info[key] = get_user_response(vk_session, user_id, question) # Получаем ответы пользователя с помощью функции get_user_response
#
#         # Запись в JSON-файл
#     try:
#         with open('questionnaires.json', 'r+') as f:
#             try:
#                 data = json.load(f)
#             except json.JSONDecodeError:
#                 data = {}
#
#             print("Data before deletion:", data)  # Вывод data до удаления
#
#             # Удаление предыдущей анкеты, если она существует
#             if user_id in data:
#                 del data[user_id]
#                 print(f"Deleted profile for user {user_id}")
#             else:
#                 print(f"No previous profile found for user {user_id}")
#
#             print("Data after deletion:", data)  # Вывод data после удаления
#
#             data[user_id] = user_info
#             f.seek(0)
#             json.dump(data, f, indent=4)
#
#     except FileNotFoundError:  # Если JSON-файл не существует
#         with open('questionnaires.json', 'w') as f:
#             json.dump({user_id: user_info}, f, indent=4)
#
#     print(f'Анкета пользователя {user_id} сохранена (предыдущая анкета удалена)!')
#     print(f'Анкета пользователя {user_id}: {user_info}')
#     for key, value in user_info.items():
#         print(f'{key}: {value}')


if __name__ == '__main__':
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            text = event.text
            if text == 'start':

                hello_message = ms.get_hello_massage(

                ).method('messages.send', post)