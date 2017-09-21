import os
from telegram.ext import Updater, CommandHandler

def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    user = update.message.from_user
    update.message.reply_text('Hello {}'.format(user.first_name))

token = os.environ['TOKEN']
updater = Updater(token=token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
