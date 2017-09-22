import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    kb_markup = ReplyKeyboardMarkup([[KeyboardButton('Хорошо, можем продолжить беседу!')],
                                    [KeyboardButton('Хотелось бы пообщаться с ним лично.')]])
    bot.send_message(chat_id=update.message.chat_id, text='Привет! Я бот-секретарь, созданный @yuraist. '
                              'Сейчас он немного занят, поэтому ты можешь пообщаться со мной. '
                              'Я передам ему всю важную информацию.', reply_markup=kb_markup)


def hello(bot, update):
    user = update.message.from_user
    update.message.reply_text('Привет, {}'.format(user.first_name))


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warning('Update "{}" caused error "{}"'.format(update, error))


def main():
    updater = Updater(token=os.environ['TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_error_handler(error)

    updater.start_polling()
