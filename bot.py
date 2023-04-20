import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from api import *
import random
import datetime
import pandas
from vk_api import VkUpload
import wikipedia

def train():
    group_id = ""
    vk_session = vk_api.VkApi(token=VKAPI)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print("Новое сообщение:")
            print("Для меня от: ", event.obj.message['from_id'])
            print("Текст :", event.obj.message['text'])
            vk.messages.send(user_id = event.obj.message['from_id'], message = "Спасибо, что написали нам. Мы обязательно ответим", random_id = random.randint(0, 2 ** 64))

def one():
    vk_session = vk_api.VkApi(token=MYVKTOKEN)# авторизуемся
    vk = vk_session.get_api()# создаем экземпляр api
    response = vk.wall.get(domain='iser_domain_or_id', count=5)# получаем последние 5 записей со стены пользователя
    for post in response['items']:
        time = datetime.datetime.fromtimestamp(post['date'])
        print("----------------")
        print(post['text'])
        print(time.strftime('%d.%m.%Y'))
        print("----------------")

def two():
    vk_session = vk_api.VkApi(token=MYVKTOKEN)
    vk = vk_session.get_api()
    friends = vk.friends.get(fields=['last_name', 'first_name', 'bdate'], order = 'last_name')# Получение списка друзей пользователя
    sorted_friends = sorted(friends['items'], key = lambda x: x['last_name'])# Сортировка друзей по фамилии
    for friend in sorted_friends:
        print(friend['last_name'], friend['first_name'], friend.get('bdate', 'Дата рождения не указана'))

def three():
    group_id = ""
    vk_session = vk_api.VkApi(VKAPI)
    vk = vk_session.get_api()
    # Создаем объект VkUpload для загрузки фотографий
    upload = VkUpload(vk_session)
    # Определяем ID основного альбома сообщества
    album_id = vk.photos.getAlbums(owner_id = group_id)['items'][0]['id']
    # Определяем список путей к файлам, которые нужно загрузить
    files = ['path/to/image1.jpg', 'path/to/image2.jpg', 'path/to/image3.jpg']
    # Загрузка фотографий
    for file in files:
        photo = upload.photo(file, album_id=album_id, group_id=group_id)
        # Публикация фотографии на стене сообщества
        vk.wall.pos(owner = group_id, attachments = f"photo{photo[0]['owner_id']}_{photo[0]['id']}")

def four():                
    group_id = ""
    vk_session = vk_api.VkApi(token = VKAPI)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)
    # функция обработки событий в longpoll
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']#response['first_name']
            user_info = vk.users.get(user_ids=user_id, fields='city')[0]
            print(user_info)
            #response = vk.users.get(user_ids = user_id, fields = ['city'])[0]
            #first_name = response['first_name']
            #city = response[0].get('city', {}).get('title', '')
            response = vk.users.get(user_ids=user_id, fields=['city'])
            if response:
                first_name = response[0]['first_name']
                city = response[0].get('city', {}).get('title', '')
                message = f'Привет, {first_name}!'
                if city:
                    message += f'Как поживает {city}?'
                vk.messages.send(peer_id=user_id, message=message, random_id=0)
            else:
                print('Не удалось получить информацию о пользователе')
            message = f'Привет, {first_name}!'
            #if city:
            #    message += f'Как поживает {city}?'
            #vk.messages.send(peer_id=user_id, message=message, random_id=0)

def five():
    group_id = ""
    vk_session = vk_api.VkApi(token = VKAPI)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)

    def get_date_and_time():
        now = datetime.datetime.now()
        date = now.strftime('%d.%m.%Y')
        time = now.strftime('%H:%M:%S')
        weekday = now.strftime('%A')
        return f"Сегодня {date}, московское время {time}, {weekday}"

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.obj.message['text'].lower()
            if any(keyword in text for keyword in ['время', 'число', 'дата', 'день']):
                message = get_date_and_time()
            else:
                message = "Я могу сообщить вам сегодняшнюю дату, московское время и день недели. Просто напишите мне об этом."
            vk.messages.send(user_id = event.obj.message['from_id'], random_id = random.randint(0, 2 ** 64), message = message)

def six():
    group_id = ""
    vk_session = vk_api.VkApi(token=VKAPI)
    vk = vk_session.get_api()
    wikipedia.set_lang('ru')
    longpoll = VkBotLongPoll(vk_session, group_id)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message_text = event.obj.message['text'].lower()
            vk.messages.send(user_id = event.obj.message['from_id'], message = 'Что бы вы хотели узнать?', random_id = random.randint(0, 2 ** 64))
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    query_text = event.obj.message['text'].lower()
                    try:
                        page = wikipedia.page(query_text)
                        message = page.content[:400] + '...'
                    except wikipedia.exceptions.PageError:
                        message = 'Информация не найдена'
                    except wikipedia.exceptions.DisambiguationError as e:
                        message = 'Найдено несколько совпадений:\n' + '\n'.join(e.options[:5])
                    
                    vk.messages.send(user_id = event.obj.message['from_id'], message = message, random_id = random.randint(0, 2 ** 64))

def seven():
    album_id = ''
    group_id = ''
    vk_session = vk_api.VkApi(token=MYVKTOKEN)
    vk = vk_session.get_api()
    photos = vk.photos.get(album_id=album_id, group_id=group_id)

    for photo in photos['items']:
        sizes = photo['sizes']
        max_size = max(sizes, key=lambda x: x['width'])
        print(f"URL: {max_size['url']}, Width: {max_size['width']}, Height: {max_size['height']}")

def eight():
    #его нельзя сделать из за ошибки
    vk_session = vk_api.VkApi(token = MYVKTOKEN)
    vk = vk_session.get_api()
    group_id = ""
    date_from = ''
    date_to = ''
    fields = 'reach'
    stats = vk.stats.get(group_id = group_id, stats_groups = 'reach', date_from = date_from, date_to = date_to)
    print(stats)

def nine():
    def get_day_of_week(date_str):
        year, month, day = map(int, date_str.split("-"))
        day_of_week = datetime.datetime(year, month, day).strftime("%A")
        return day_of_week
    def send_message(user_id, message):
        vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=vk_api.utils.get_random_id()
        )
    group_id = ""
    vk_session = vk_api.VkApi(token = VKAPI)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message['text'].lower()
            user_id = event.obj.message['from_id']
            if "какой день недели была" in message:
                try:
                    date_str = message.split('была ')[1].strip()
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    date = datetime.datetime.strftime(date_obj, '%Y-%m-%d')
                    weekday = get_day_of_week(date_str)
                    send_message(user_id, f"{date_str} была {weekday}")
                except:
                    send_message(user_id, "Некорректный формат даты, введите дату в формате yyyy-mm-dd")
            else:
                send_message(user_id, "Я могу сказать, в какой день недели была какая-нибудь дата, напишите 'какой день недели была 'нужная дата'")

def ten():
    url = 'https://google.ru/maps/search/'
    group_id = ""
    vk_session = vk_api.VkApi(token=VKAPI)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            country = event.obj.message['text']
            vk.messages.send(peer_id = user_id, message = f"Ваш город доступен по ссылке: {url + country}", random_id = vk_api.utils.get_random_id())

def my_bot():
    group_id = ""
    vk_session = vk_api.VkApi(token=VKAPI)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)
    kotiki =[
            'https://klike.net/uploads/posts/2022-06/1654842544_1.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842566_2.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842597_3.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842644_4.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842544_1.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842544_1.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842616_7.jpg',
            'https://klike.net/uploads/posts/2022-06/1654842573_8.jpg']
    message = kotiki[random.randint(0, 7)]
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            vk.messages.send(user_id = user_id, message = message, random_id = vk_api.utils.get_random_id())
    

if __name__ == "__main__":
    print('OKEY LETS GO')
    my_bot()