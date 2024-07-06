import telebot.apihelper
from telebot import TeleBot
from misc.answers import *
from services.RAGFlow import RagFlow
from requests import exceptions
from config import Config
import os

apikey = Config.TELEGRAM_API
bot = TeleBot(
    apikey
)
flow = RagFlow()
commands = [
    '/start',
    '/help',
    '/upload_file'
]

@bot.message_handler(commands=['start'])
def start(message):
    rustore_logo = open('media/RuStore_Logo.jpg', 'rb')
    bot.send_photo(message.chat.id, rustore_logo, caption=assistant_entry)

@bot.message_handler(commands=['help'])
def help(message):
    rustore_logo = open('media/QA_logo.jpg', 'rb')
    bot.send_photo(message.chat.id, rustore_logo, caption=assistant_help)

@bot.message_handler(commands=['upload_file'])
def upload_file(message):
    print('\n [TG] Recieved attempt to upload')
    process_logo = open('media/processing.jpeg', 'rb')
    bot.send_photo(message.chat.id, process_logo, caption=assistant_files)

    def file_load(message):
        print('[TG] Loading file')
        bot.send_message(message.chat.id, "Получил ваш файл! Скачиваю его себе...")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        print(f'[TG] Recieved file. {message.document.file_name}')

        if 'data' not in os.listdir('.'):
            print('[TG] Making data directory')
            os.mkdir('data')

        with open('data/' + message.document.file_name, 'wb') as file:
            file.write(downloaded_file)

        cwd = os.getcwd()
        print(f'[TG] Loading files to RagFLOW {os.path.join(cwd, 'data', message.document.file_name)}')
        flow.load_files(
            file= os.path.join(cwd, 'data/', message.document.file_name),
            knowledge_base='main'
        ) # Непонятно какой формат file.

        process_logo = open('media/processing.jpeg', 'rb')
        bot.send_photo(message.chat.id, process_logo, caption=assistant_files_success)

    bot.register_next_step_handler(message, file_load)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text not in commands:

        print(f'\n[TG] Got Query: {message.text}')
        conv_id = flow.make_conversation(
            tg_userid = message.json.get('from').get('id')
        )

        print('[TG] Pulling Answer')
        answer = flow.get_answer(message.text, conv_id)
        if answer == None:
            conv_id = flow.make_conversation(
                tg_userid = message.json.get('from').get('id'),
                force = True
            )
            answer = flow.get_answer(message.text, conv_id)
        print('[TG] Sending Message')
        bot.send_message(message.chat.id, answer)
        print('[TG] Query answered \n -=-=-=-=-=-=-=-=-=-')

try:
    bot.infinity_polling()
except exceptions.ReadTimeout as err:
    print(err)
    bot.infinity_polling()