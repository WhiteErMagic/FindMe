from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api

from vk_api.utils import get_random_id
from search_criteria import create_user_criteria

from VKRepository import VKRepository
from  main import get_user_response, create_user_profile

session = vk_api.VkApi(token='vk1.a.BIz9EanDLhQLtuSTT5mVGSTvU7mIycKbGSzDDIVisPwVFO7VwFuglk4c8Z87XC1M0dS_fkkVsCll42WTCH5toPeEabcYTxCz6C7gqoLgTEKd6DrSD9uU0tofY8S3AhXZp_1Ln18-CKTWtrRn81IG18MBY2KAMrAIE3L_DuKKkNiW3sKzPQkdScH722rzshSP5asvFd_daoETjY_-2CzvSg')
longpoll = VkLongPoll(session)
def send_message(user_id, message, keyboard= None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id()
    }
    if keyboard:
        post['keyboard'] = keyboard.get_keyboard()
    session.method('messages.send', post)

if __name__ == '__main__':
    vk_reposiroty = VKRepository()
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            text = event.text.lower()
            user_id = event.user_id
            user_info = session.method('users.get', {'user_ids': user_id})[0]
            first_name = user_info['first_name']
            # first_name = vk_reposiroty.get_user_first_name(user_id)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('start', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('хочу зарегистрироваться', color=VkKeyboardColor.POSITIVE)
            if text == "start":
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Хочу зарегистрироваться', color=VkKeyboardColor.POSITIVE)
                send_message(user_id, f'🚀 Привет, {first_name}!  👋  Я – бот, который экономит '
                                      f'твое время и помогает найти любовь быстро и легко! '
                                      f' ⏱️  Хочешь зарегистрироваться и начать поиск своей второй половинки?  💖', keyboard)
            if text == "хочу зарегистрироваться":
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Создание анкеты', color=VkKeyboardColor.POSITIVE)
                send_message(user_id, f'Здорово! 😊  Чтобы подобрать тебе идеальную пару, мне потребуется немного информации о твоих предпочтениях.'
                                      f' 🔐  Не волнуйся, все данные останутся конфиденциальными. 😉', keyboard)

            if text == "создание анкеты":
                keyboard = VkKeyboard(one_time=False)



                keyboard.add_button('Создать критерии', color=VkKeyboardColor.POSITIVE)

                keyboard.add_button('Поиск', color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                keyboard.add_button('Изменить анкету', color=VkKeyboardColor.NEGATIVE)
                create_user_profile(user_id, session)
                send_message(user_id, 'Ура, твоя анкета создана! 🥳 \n\n'
                                      'Можешь сразу начать поиск по умолчанию, который использует твой возраст и город, нажав "Поиск". \n\n'
                                      'А если хочешь что-то особенное, нажми "Создать критерии" и мы найдём тебе идеальных кандидатов! 💥 \n'
                                      'Кстати, ты всегда можешь изменить свою анкету в разделе "Изменить анкету".'
                                      'Желаем тебе найти свою родственную душу! ❤️🌸   ', keyboard)

            if text == "Создать критерии":
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('Изменить критерии', color=VkKeyboardColor.POSITIVE)
                create_user_criteria(user_id, session)
                send_message(user_id, 'Критерии созданы! 🥳 В любой момент вы можете их изменить нажам на кнопку "Изменить критерии"\n\n', keyboard)
            if text == "Изменить анкету":
                create_user_profile( user_id, session)
                send_message(user_id, 'Анкета изменена! 🥳 \n\n')
                    # кнопка фаворитов  черный список
                    # кнопка вперед

            if text == "Поиск":
                pass
                    #users_list = vk_repository.get_users_list(criteria_dict)
                    # вывод первого кандидата  фото имя фамилия возраст город
