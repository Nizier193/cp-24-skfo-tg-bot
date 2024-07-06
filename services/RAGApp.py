import requests
import sys
import os

sys.path.append('..')
from config import Config

class RagAPP():
    url = Config.RAGAPP_URL

    def __init__(self):
        pass

    def add_file(self, filename):
        url = self.url + 'management/files'
        # Замените 'file_path' на путь к файлу, который вы хотите загрузить
        try:
            files = {'file': open(os.path.join(Config.FILEBASE, filename), 'rb')}

            print('[FLOW] Posting request to API')
            response = requests.post(url, files=files)

            if response.status_code == 200:
                print("[FLOW] File uploaded successfully!")

            else:
                print(f"[FLOW] Failed to upload file with status code: {response.status_code}")
        except Exception as err:
            print(err)

        return  # Все файлы

    def request(self, question):
        print(f'[FLOW] Got query {question}')
        url = Config.RAGAPP_URL + 'chat/request'  # URL для отправки запроса
        headers = {'Content-Type': 'application/json'}  # Устанавливаем заголовок Content-Type

        # Создаем тело запроса в формате JSON
        payload = {
            "messages": [
                {
                    "content": question,
                    "role": "user"
                }
            ]
        }

        print('[FLOW] Posting request to API')
        # Отправляем POST запрос к API
        response = requests.post(url, json=payload, headers=headers)
        print(f'[FLOW] Got response {response.json().get('result').get('content')}')
        return response.json().get('result').get('content')

    def get_files(self):
        url = self.url + 'management/files'
        return requests.get(url).json()