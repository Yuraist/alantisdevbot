import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    user = update.message.from_user
    update.message.reply_text('Hello {}'.format(user.first_name))


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

token = os.environ['TOKEN']
updater = Updater(token=token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
