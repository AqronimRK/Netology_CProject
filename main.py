from Modules.VK import FromVK
from Modules.Yandex import ToYandex
from Modules import VK
from pprint import pprint
from datetime import datetime
import json

vk_id_input = input('Введите id или короткое имя пользователя: ')
vk_user = FromVK(vk_id_input)
pprint(vk_user.get_albums())
while True:
    vk_album_id = int(input('Введите id альбома из списка выше: '))
    if vk_album_id in vk_user.get_albums().values():
        break
    else:
        print('Введен некорректный id альбома!')

count_photo_in_album = vk_user.get_photo(vk_album_id, count_photo=5)["count"]

while True:
    count_choose = input(f'Хотите выбрать количество фото для выгрузки (по умолчанию 5) и не более '
                         f'{count_photo_in_album}? Y/N: ').upper()
    if count_choose == 'Y':
        while True:
            count_photo = input('Введите количество: ')
            if VK.isint(count_photo):
                if int(count_photo) <= count_photo_in_album:
                    break
                else:
                    print('Превышено количество фото или неверный ввод!')
            else:
                print('Введите число!y')
        break
    elif count_choose == 'N':
        count_photo = 5
        break
    else:
        print('Исправьте ответ!')

photo_user_dict = vk_user.get_photo(vk_album_id, count_photo)['items']

likes_url_dict = {}
json_list = []
like_list = []

for photo in photo_user_dict[:int(count_photo)]:
    likes = photo['likes']['count']
    date = datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d-%HH-%MM-%SS')
    size = photo['sizes'][-1]['type']
    photo_url = photo['sizes'][-1]['url']
    if f'{likes}.jpg' not in like_list:
        likes_url_dict[f'{likes}.jpg'] = photo_url
        json_list.append({'file_name': f'{likes}.jpg', 'size': size})
        like_list.append(f'{likes}.jpg')
    else:
        likes_url_dict[f'{likes} {date}.jpg'] = photo_url
        json_list.append({'file_name': f'{likes} {date}.jpg', 'size': size})

with open('ResultJSON/photo_data.json', 'w') as datafile:
    json.dump(json_list, datafile, indent=4)

yandex_token = input('Введите токен для доступа к Яндекс.Диску: ')
yandex_user = ToYandex(yandex_token)
yandex_user.upload_photo(likes_url_dict)
