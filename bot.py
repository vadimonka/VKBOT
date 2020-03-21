import requests
import vk_api
import pyowm
import math
import wikipedia
#авторизуемся как сообщество
vk_session = vk_api.VkApi(token='5a441939e0690d2e476fdff704e8774d8afed00d6fe7e5ed66386aad0134fd3b5085838275f6b30dbe7a1')
#подключаемся к сервису погоды
owm = pyowm.OWM('bd83f5a4de08a8c7be114865ec1aca16', language="ru")
#устанавливаем поиск по русскоязычной версии википедии
wikipedia.set_lang("RU")

from vk_api.longpoll import VkLongPoll, VkEventType
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:		
        if event.from_user: #Если написали в ЛС
            event.text=event.text.lower()
            tf = event.text.find('?')
            wiki = event.text[0:-1]
            if event.text == 'привет' or event.text == 'здарова' or event.text == 'здравствуй': #Если написали заданную фразу
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    random_id=event.random_id,
                    message='И тебе здарова, гусь'
                )
            elif tf>0:
                try:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=event.random_id,
                        message='Вот что я нашёл:\n' + str(wikipedia.summary(wiki))
                    )
                except wikipedia.exceptions.DisambiguationError as e:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=event.random_id,
                        message=e.options
                    )
                except wikipedia.exceptions.PageError:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=event.random_id,
                        message='Ничего не найдено'
                    )
            else:
                try:
                    observation = owm.weather_at_place(event.text)
                    w = observation.get_weather()
                    temp = w.get_temperature('celsius')['temp']
                    temp = math.trunc(temp)
                    if temp < 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='В городе ' + event.text + ' ' + w.get_detailed_status() + '\
                            \nТемпература в районе ' + str(temp) + '°\
                            \nСейчас ппц как холодно, одевайся как танк епта!'
                        )
                    elif temp < 21:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='В городе ' + event.text + ' ' + w.get_detailed_status() + '\
                            \nТемпература в районе ' + str(temp) + '°\
                            \nСейчас прохладно, надень ветровку.'
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='В городе ' + event.text + ' ' + w.get_detailed_status() + '\
                            \nТемпература в районе ' + str(temp) + '°\
                            \nТемпература огонь, но бабушкины труселя всё равно пригодятся.'
                        )
                except:
                    vk.messages.send(
                            user_id=event.user_id,
                            random_id=event.random_id,
                            message='Я пока не умею отвечать на такое...ноо если хочешь узнать погоду - введи название ближайшего города.'
                    )
        '''elif event.from_chat: #Если написали в Беседе
            vk.messages.send( #Отправляем собщение
                chat_id=event.chat_id,
                message='Всем кулити'
            )'''
