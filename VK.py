import requests
from datetime import datetime
import json
from pprint import pprint


with open('VKToken.txt') as vk:
    vk_token = vk.readline().strip()


class FromVK:
    def __init__(self):
        self.vk_query = 'https://api.vk.com/method'
        self.params = {
            'access_token': vk_token,
            'v': 5.131
        }

    @staticmethod
    def isint(id_str):
        try:
            int(id_str)
            return True
        except ValueError:
            return False

    def _get_id(self):
        vkid = input('Введите id или короткое имя пользователя: ')
        if self.isint(vkid):
            return int(vkid)
        else:
            get_id_param = {'user_ids': vkid}
            query = f'{self.vk_query}/users.get'
            user_id = requests.get(query, params=self.params | get_id_param).json()['response'][0]['id']
            return user_id

    def _get_albums(self, owner_id: int):
        get_albums_params = {'owner_id': owner_id, 'need_system': 1}
        query = f'{self.vk_query}/photos.getAlbums'
        albums_items = requests.get(query, params=self.params | get_albums_params).json()['response']['items']
        albums_id = {albums_items[i]['title']: albums_items[i]['id'] for i in range(len(albums_items))}
        return albums_id

    def get_photo(self, count_photo=5):
        account = self._get_id()
        pprint(self._get_albums(account))
        album_id = input('Введите id альбома из списка выше: ')

        get_photo_params = {
            'owner_id': account,
            'album_id': str(album_id),
            'rev': 1,
            'extended': 1,
            'photo_size': 1,
        }

        count_photo = int(input('Введите количество фото для выгрузки: '))
        query = f'{self.vk_query}/photos.get'
        items = requests.get(query, params=self.params | get_photo_params).json()['response']['items']
        likes_url_dict = {}
        json_list = []
        like_list = []

        for photo in items[:count_photo]:
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

        with open('photo_data.json', 'w') as datafile:
            json.dump(json_list, datafile, indent=4)
        return likes_url_dict
