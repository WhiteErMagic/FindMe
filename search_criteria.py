import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id




token = "vk1.a.BIz9EanDLhQLtuSTT5mVGSTvU7mIycKbGSzDDIVisPwVFO7VwFuglk4c8Z87XC1M0dS_fkkVsCll42WTCH5toPeEabcYTxCz6C7gqoLgTEKd6DrSD9uU0tofY8S3AhXZp_1Ln18-CKTWtrRn81IG18MBY2KAMrAIE3L_DuKKkNiW3sKzPQkdScH722rzshSP5asvFd_daoETjY_-2CzvSg"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)


def get_user_criteria(vk_session, user_id, message):
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id()
    })
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            return event.text

def create_user_criteria(user_id, vk_session):
    criteria = {}

    questions = {

        "sex" : "Какой пол тебя интересует?(1 - женский, 2 - мужской, 0 - оба)",
        "age_from" : "От какого возраста?",
        "age_to" : "До какого возраста?",
        "city" : " В каком городе ищем?",
        "relation": "В каком статусе он ? (1-  не женат/не замужем, 2 - есть друг/есть подруга, 3 - помолвлен/помолвлена, 4 - женат/замужем, 5 - всё сложно, 6 - в активном поиске, 7 - влюблен/влюблена, 8 - в гражданском браке)"
    }
    for key, question in questions.items():
        criteria[key] = get_user_criteria(vk_session, user_id, question)
    try:
        with open('criteria_selection.json', 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

            print("Data before deletion:", data)  # Вывод data до удаления



            # Удаление предыдущей анкеты, если она существует
            if user_id in data:
                del data[user_id]
                print(f"Deleted criteria for user {user_id}")
            else:
                print(f" No criteria for user {user_id}")
                # Вывод data после удаления

            data[user_id] = criteria
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()
            print("Data after deletion:", data)  # Вывод data после удаления
    except FileNotFoundError:
        with open('criteria_selection.json', 'w') as f:
            json.dump({user_id: criteria}, f, indent=2, ensure_ascii=False)

    print(f'Критерии пользователя {user_id} сохранена ')
    print(f'Критерии пользователя {user_id} : {criteria}')





