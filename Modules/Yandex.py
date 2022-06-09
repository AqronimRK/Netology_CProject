import requests
from progress.bar import IncrementalBar


class ToYandex:
    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.yandex_headers = {'Content-type': 'application/json', 'Authorization': f'OAuth {self.ya_token}'}

    def _create_direct(self, directory_name=''):
        directory_name = input('Введите имя папки для создания: ')
        params = {'path': directory_name}
        dir_query = 'https://cloud-api.yandex.net/v1/disk/resources/'
        requests.put(dir_query, headers=self.yandex_headers, params=params)
        return directory_name

    def upload_photo(self, files):
        upload_query = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        directory = self._create_direct()
        status_bar = IncrementalBar('Upload process', max=len(files))
        for name, upload_url in files.items():
            params = {'path': f'/{directory}/{name}', 'url': upload_url}
            requests.post(upload_query, headers=self.yandex_headers, params=params)
            status_bar.next()
        status_bar.finish()
