import requests
import vk_api
import json

vk_session = vk_api.VkApi(token='')

from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:			
        if event.text == 'Начать': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    message='Привет\nЯ бот для расчёта ежемесячного платежа по ипотеке\n\nДля работы, мне нужны данные\nДля начала введи ФИО',
                    random_id=0
                )
        else:
            print(event.user_id)
            with open(str(event.user_id)+'.txt', 'r+', encoding='utf-8') as f:
                print('Файл открылся')
                #f.write('first line' + '\n')
                data = json.loads(f.read())
                print(data)
            f.close()
            print('Закрываем файл')