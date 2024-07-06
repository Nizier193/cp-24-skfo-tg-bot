import telebot.apihelper
from telebot import TeleBot
from misc.answers import *
from services.RAGFlow import RagFlow
from services.RAGApp import RagAPP
from requests import exceptions
from config import Config, Providers
import os

apikey = Config.TELEGRAM_API
bot = TeleBot(
    apikey
)
flow = RagAPP()
commands = [
    '/start',
    '/help',
    '/upload_file',
    '/files_get'
]

@bot.message_handler(commands=['start'])
def start(message):
    rustore_logo = open('media/RuStore_Logo.jpg', 'rb')
    bot.send_photo(message.chat.id, rustore_logo, caption=assistant_entry)

@bot.message_handler(commands=['help'])
def help(message):
    rustore_logo = open('media/QA_logo.jpg', 'rb')
    bot.send_photo(message.chat.id, rustore_logo, caption=assistant_help)
    bot.send_message(message.chat.id, assistant_config)

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

        if Config.FILEBASE[:-1] not in os.listdir('.'):
            print('[TG] Making data directory')
            os.mkdir(Config.FILEBASE)

        with open(Config.FILEBASE + message.document.file_name, 'wb') as file:
            file.write(downloaded_file)

        print(f'[TG] Loading files to RagAPP {os.path.join(Config.FILEBASE, message.document.file_name)}')
        flow.add_file(
            filename=os.path.join(
                message.document.file_name
            )
        )
        print('[TG] Files added to RagAPP')

        process_logo = open('media/processing.jpeg', 'rb')
        bot.send_photo(message.chat.id, process_logo, caption=assistant_files_success)

    bot.register_next_step_handler(message, file_load)

@bot.message_handler(commands=['files_get'])
def answer(message):
    str_ = '\n'.join([str(index + 1) + ". " + name.get('name') for index, name in enumerate(flow.get_files())])
    bot.send_message(message.chat.id, "Все файлы, которые есть в системе: \n" + str_)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text not in commands:
        answer = flow.request(message.text)
        print('[TG] Sending Message')
        bot.send_message(message.chat.id, answer)
        print('[TG] Query Answered')

try:
    bot.infinity_polling()
except exceptions.ReadTimeout as err:
    print(err)
    bot.infinity_polling()