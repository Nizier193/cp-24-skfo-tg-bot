import requests
import sys
import random

sys.path.append('services/')
sys.path.append('..')
from database import UserDatabase
from config import Config

db = UserDatabase()
db.create_table()

class RagFlow:
    def __init__(self):
        self.apikey = Config.RAGFLOW_API
        self.endpoint = Config.RAGFLOW_URL

    def make_conversation(self, tg_userid: int, force: bool = False):
        print('[FLOW] Pulling conversation')
        try:
            headers = {
                'Authorization': f'Bearer {self.apikey}',
                'Content-Type': 'application/json'
            }
            data = {
                'user_id': str(tg_userid)
            }

            if not force:
                if db.get_conv(tg_userid) == None:
                    print(f'User not found ✖')
                    ans = requests.get(self.endpoint + 'new_conversation/', headers=headers, params=data).json()
                    conv_id = ans.get('data').get('id')
                    db.add_user(tg_userid, conv_id)

                    print('[FLOW] User added to database')
                else:
                    print(f'[FLOW] User found ✔')
                    conv_id = db.get_conv(tg_userid)[-1]
                    print('[FLOW] User is in database')
            else:
                print('[FLOW] Force adding user to database')
                db.delete_cond(tg_userid)
                ans = requests.get(self.endpoint + 'new_conversation/', headers=headers, params=data).json()
                conv_id = ans.get('data').get('id')
                db.add_user(tg_userid, conv_id)
                print('[FLOW] Force added user')

        except Exception as err:
            print(err)
            return None

        print(f'[FLOW] Pulled conv_id: {conv_id}')
        return conv_id

    def get_answer(self, query: str, conv_id: str):
        print(f'[FLOW] Got query: {query}')
        print('[FLOW] Pulling answer')
        try:
            headers = {
                'Authorization': f'Bearer {self.apikey}',
                'Content-Type': 'application/json'
            }
            data = {
                'conversation_id': conv_id,
                'messages': [
                    {"role": "user", "content": query}
                ],
                'stream': False,
            }
            print('[FLOW] Posting request to endpoint')
            ans = requests.post(
                self.endpoint + 'completion/', json=data, headers=headers
            )
            print('[FLOW] Got an answer below...')
            print(ans.json())

            if ans.json().get('data') == None:
                answer = ans.json()
                if answer['retcode'] == 102:
                    return None

            return ans.json().get('data').get('answer')
        except Exception as err:
            print('[FLOW] Got an error while pulling answer')
            return str(err)

    def load_files(self, file, knowledge_base='main'):
        print('[FLOW] Sending request')
        try:
            headers = {
                'Authorization': f'Bearer {self.apikey}',
                'Content-Type': 'application/json'
            }
            data = {
                'file': file,
                'kb_name': knowledge_base,
                'run': '1',
            }
            requests.post(self.endpoint + 'document/upload', json=data, headers=headers)
            print('[FLOW] Added file')
        except Exception as err:
            return err

    def dummy_answer(self, stuff):
        answers = {
            1: "Hi, I do actually work!",
            2: "I`m RuStore Telebot",
            3: "I do work by Pytelegrambotapi"
        }
        return answers.get(random.randint(1, 3)) + f"\n{self.apikey} \n{self.endpoint} \n{stuff}"
