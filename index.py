import requests
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

print("Запуск ...")

vk_session = vk_api.VkApi(token='')

from vk_api.longpoll import VkLongPoll, VkEventType

print("Библиотеки запущены")

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

print("Бот запущен")

for event in longpoll.listen():   
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    #Слушаем longpoll, если пришло сообщение то:			
        if event.text == 'Начать': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    message='&#128075; Привет\n&#128184; Я бот для расчёта ежемесячного платежа по ипотеке (аннуитетный вид)\n\n&#128203; Для работы, мне нужны данные\nДля начала введите ФИО',
                    random_id=0
                )
        else:
            print(event.user_id)
 
            try:
                file = open(str(event.user_id)+'.txt', 'r+', encoding='utf-8')
                
                print("Файл есть")
                
                data = json.loads(file.read())
                print(data)
                
                if(('FIO' in data) == False):
                    #ФИО не введено
                    print('Нет ФИО у id', str(event.user_id))
                    data['FIO'] = str(event.text)
                
                    vk.messages.send( #Отправляем сообщение
                        user_id=event.user_id,
                        message='&#128515; Отлично\n&#128241; Введите номер телефона',
                        random_id=0
                    )
                elif(('phone' in data) == False):
                    #Ноиер телефона не введён
                    print('Нет номера у id', str(event.user_id))
                    data['phone'] = str(event.text)
                
                    keyboard = VkKeyboard()
                    keyboard.add_button('Добавить объект', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_line()
                    keyboard.add_button('Показать предыдущие', color=VkKeyboardColor.PRIMARY)
                
                    vk.messages.send( #Отправляем сообщение
                        user_id=event.user_id,
                        message='&#128519; Превосходно\n&#127873; Теперь вы можете ввести данные для расчёта ипотеки, нажав кнопку "Добавить объект"', 
                        keyboard=keyboard.get_keyboard(),
                        random_id=0
                    ) 
                else:
                    #Необходимые данные введены
                    print('У пользователя с id', str(event.user_id), ' введены необходимые данные')
                    
                    if(event.text == "Добавить объект"):
                        #Пользоватлеь добавляет объект
                        
                        if(('objects' in data) == False):
                            #Объекты ранее не добавлялись
                            data['objects'] = []
                        
                        if((('act' in data) == False) or (data['act'] == "free")):
                            #Добавление не занято
                            data['act'] = 1
                            data['temp_object'] = []
                            vk.messages.send( #Отправляем сообщение
                                user_id=event.user_id,
                                message='&#127968; Для начала введите наименование объекта (пример: Квартира)', 
                                random_id=0
                            ) 
                        else:
                            #Уже добавляется объект, удаляем его
                            data['act'] = 1
                            data['temp_object'] = []
                            vk.messages.send( #Отправляем сообщение
                                user_id=event.user_id,
                                message='Уже добавляется объект\n Удаляем ранние настройки и создаём новые\n\n&#127968; Для начала введите наименование объекта (пример: Квартира)', 
                                random_id=0
                            )
                    elif(event.text == "Показать предыдущие"):
                        #Показать раннее добавленные объекты
                        if(('objects' in data) == False):
                            #Объекты ранее не добавлялись
                            data['objects'] = []
                            vk.messages.send( #Отправляем сообщение
                                user_id=event.user_id,
                                message='Вы ещё не добавили ни одного объекта', 
                                random_id=0
                            ) 
                        else:
                            textsend = "&#128203; Вот всё объекты:"
                            for object in data['objects']:
                                textsend = textsend + "\n\n&#127968; Название объекта: " + object['name'] + "\n&#128184; Цена: " + object['price'] + "₽\n&#128176; Первоначальный взнос: " + object['contribution'] + "₽\n&#9851; Процентная ставка: " + object['bid'] + "%\n&#128197; Срок ипотеки: " + object['term'] + "\n&#128200; Ежемесячный платёж: " + object['mortgage'] + "₽"
                            #Объекты добавлялись
                            vk.messages.send( #Отправляем сообщение
                                user_id=event.user_id,
                                message=textsend, 
                                random_id=0
                            )
                    else:    
                        print("что то другое")
                        #Пользователь просто пишет
                        if((('act' in data) == False) or (data['act'] == "free")):
                            print("что то другое 1")
                            #Объекты не создавались
                            keyboard = VkKeyboard()
                            keyboard.add_button('Добавить объект', color=VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button('Показать предыдущие', color=VkKeyboardColor.PRIMARY)
                        
                            vk.messages.send( #Отправляем сообщение
                                user_id=event.user_id,
                                message='&#127873; Введите данные для расчёта ипотеки\n&#127968; Для начала введите наименование объекта (пример: Квартира)', 
                                keyboard=keyboard.get_keyboard(),
                                random_id=0
                            )
                        else:
                            print("что то другое 2 (",data['act'],") (",type(data['act']),")")
                            #Создаётся объект, проверяем этап
                            try:
                                if(str(data['act']) == "1"):
                                    #Ввели название объекта
                                    data['act'] = 2
                                    data['temp_object'].append(event.text)
                                    vk.messages.send( #Отправляем сообщение
                                        user_id=event.user_id,
                                        message='Введите стоимость объекта', 
                                        random_id=0
                                    )
                                elif(str(data['act']) == "2"):
                                    #Ввели стоимость объекта
                                    data['act'] = 3
                                    data['temp_object'].append(event.text)
                                    vk.messages.send( #Отправляем сообщение
                                        user_id=event.user_id,
                                        message='Введите первоначальный взнос', 
                                        random_id=0
                                    )
                                elif(str(data['act']) == "3"):
                                    #Ввели первоначальный взнос
                                    data['act'] = 4
                                    data['temp_object'].append(event.text)
                                    vk.messages.send( #Отправляем сообщение
                                        user_id=event.user_id,
                                        message='Введите годовую процентную ставку', 
                                        random_id=0
                                    )
                                elif(str(data['act']) == "4"):
                                    #Ввели процентную ставку
                                    data['act'] = 5
                                    data['temp_object'].append(event.text.replace(",",".").replace("%",""))
                                    vk.messages.send( #Отправляем сообщение
                                        user_id=event.user_id,
                                        message='Введите срок ипотеки в месяцах', 
                                        random_id=0
                                    )
                                elif(str(data['act']) == "5"):
                                    #Ввели срок ипотеки
                                    #https://myoffice.ru/blog/kak-rasschitat-ipoteku-samostoyatelno/
                                    data['act'] = "free"
                                    data['temp_object'].append(event.text)
                                    mortgage = ((float(data['temp_object'][3])/12)/100)
                                    mortgagesc = (1+mortgage)**float(data['temp_object'][4])
                                    mortgage = (float(data['temp_object'][1])-float(data['temp_object'][2]))*((mortgage*mortgagesc)/(mortgagesc - 1))
                                    mortgage = round(mortgage,2)
                                    vk.messages.send( #Отправляем сообщение
                                        user_id=event.user_id,
                                        message='По введёным расчётам, вам придётся платить за ипотеку '+str(mortgage)+'₽ каждый месяц', 
                                        random_id=0
                                    )
                                    data['objects'].append({"name":data['temp_object'][0],"price":data['temp_object'][1],"contribution":data['temp_object'][2],"bid":data['temp_object'][3],"term":data['temp_object'][4],"mortgage":str(mortgage)})
                                    data['temp_object'] = []
                                else:
                                    data['act'] = "free"
                                    data['temp_object'] = []
                                    vk.messages.send( #Отправляем сообщение
                                        user_id=event.user_id,
                                        message='UPS :/\nКакая-то ошибка', 
                                        random_id=0
                                    )
                                    
                            except:
                                data['act'] = "free"
                                data['temp_object'] = []
                                vk.messages.send( #Отправляем сообщение
                                    user_id=event.user_id,
                                    message='Значения должны быть числовые', 
                                    random_id=0
                                )
                            
                    
                file = open(str(event.user_id)+'.txt', 'w+', encoding='utf-8')
                file.write(json.dumps(data, ensure_ascii=False))
                
            except Exception as err:
                #Файла нет, создаём
                file = open(str(event.user_id)+'.txt', 'w+', encoding='utf-8')
                
                print("Файла нет")
            
                data = {'FIO':str(event.text)}
                file.write(json.dumps(data, ensure_ascii=False))
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    message='&#128515; Отлично\n&#128241; Введите номер телефона',
                    random_id=0
                )
                print("Ошибка чтения файла ", err, ". Создаю новый")
                print(data)
            
            file.close()
            print('Закрываем файл\n')