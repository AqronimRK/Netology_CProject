from VK import FromVK
from Yandex import ToYandex

if __name__ == '__main__':
    data_files = FromVK().get_photo()
    upload_to_yandex = ToYandex().upload_photo(data_files)
