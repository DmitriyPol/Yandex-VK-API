import requests
import os
from time import sleep
from tqdm import tqdm, tqdm_gui, trange
import json
os.chdir(r'C:\\VSCode\\Netology\\Kursovaya')

from pprint import pprint

class PhotoVK:

    def getphoto(self, id):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id' : id,
            'album_id' : 'profile',
            'extended' : 1,
            'access_token' : tokenvk,
            'v':'5.131'
        }
        data = {}
        res = requests.get(URL, params=params)
        info = res.json()
        with open('data.json', 'w') as f:
            json.dump(info, f)
        data.update(res.json())
        my_dict = {}
        data_dict = {}
        data_list = []
        my_list = []
        for i in range(len(data['response']['items'])):
            name = data['response']['items'][i]['likes']['count']
            size = data['response']['items'][i]['sizes'][-1]['type']
            url = data['response']['items'][i]['sizes'][-1]['url']
            data_dict = ({'file_name' : str(name) + '.jpg', 'size' : size})
            my_dict = ({'file_name' : str(name) + '.jpg', 'size' : size, 'url' : url})
            data_list.append(data_dict)
            my_list.append(my_dict)
        pprint(data_list)
        return my_list

class YaUploader:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload(self, data_list):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for i in trange(len(data_list)):
            file_name = data_list[i]['file_name']
            size = data_list[i]['size']
            url = data_list[i]['url']
            params = {'path' : f'{path}/{file_name}', 'url' : url, 'disable_redirects' : False}
            response = requests.post(url = upload_url, headers=headers, params = params)
            response.raise_for_status()
            if response.status_code == 201:
                print('Success')

    def create_path(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {'path' : f'Photo id {str(id)}'}
        response = requests.put(url = url, headers = headers, params = params)
        if response.status_code == 201:
            print('Created')
        return f'Photo id {str(id)}'

if __name__ == '__main__':
    id = int(input('Введите id:'))
    token_ya = str(input('Введите токен с Полигона Яндекс.Диска:'))
    data_photo = PhotoVK()
    uploader = YaUploader(token_ya)
    result = data_photo.getphoto(id)
    path = uploader.create_path()
    new_result = uploader.upload(result)