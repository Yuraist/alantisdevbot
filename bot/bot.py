import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    user = update.message.from_user
    update.message.reply_text('Hello {}'.format(user.first_name))


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
