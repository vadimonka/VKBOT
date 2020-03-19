import requests
import vk_api
import pyowm
import math
#авторизуемся как сообщество
vk_session = vk_api.VkApi(token='5a441939e0690d2e476fdff704e8774d8afed00d6fe7e5ed66386aad0134fd3b5085838275f6b30dbe7a1')
#подключаемся к сервису погоды
owm = pyowm.OWM('bd83f5a4de08a8c7be114865ec1aca16', language="ru")

from vk_api.longpoll import VkLongPoll, VkEventType
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:		
        if event.from_user: #Если написали в ЛС
            event.text=event.text.title()
            if event.text == 'Привет' or event.text == 'Здарова' or event.text == 'Здравствуй': #Если написали заданную фразу
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    random_id=event.random_id,
                    message='И тебе здарова, гусь'
                )
            else:
                try:
                    observation = owm.weather_at_place(event.text)
                    w = observation.get_weather()
                    temp = w.get_temperature('celsius')['temp']
                    temp = math.trunc(temp)
                    if temp < 0:
                        vk.messages.send( #Отправляем сообщение
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='В городе ' + event.text + ' ' + w.get_detailed_status() + '\n\
                            Температура в районе ' + str(temp) + '°\n\
                            Сейчас ппц как холодно, одевайся как танк епта!'
                        )
                    elif temp < 21:
                        vk.messages.send( #Отправляем сообщение
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='В городе ' + event.text + ' ' + w.get_detailed_status() + '\n\
                            Температура в районе ' + str(temp) + '°\n\
                            Сейчас прохладно, надень ветровку.'
                        )
                    else:
                        vk.messages.send( #Отправляем сообщение
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='В городе ' + event.text + ' ' + w.get_detailed_status() + '\n\
                            Температура в районе ' + str(temp) + '°\n\
                            Температура огонь, но бабушкины труселя всё равно пригодятся.'
                        )
                except:
                    vk.messages.send( #Отправляем сообщение
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='Я пока не умею отвечать на такое...ноо если хочешь узнать погоду - введи название ближайшего города.'
                    )
        '''elif event.from_chat: #Если написали в Беседе
            vk.messages.send( #Отправляем собщение
                chat_id=event.chat_id,
                message='Всем кулити'
            )'''