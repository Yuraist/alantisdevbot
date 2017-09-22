import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

from app import db
from app.models import User, Order

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def keyboard_markup(phrases):
    button_list = []
    for phrase in phrases:
        button_list.append([KeyboardButton(phrase)])

    markup = ReplyKeyboardMarkup(button_list, one_time_keyboard=True)
    return markup


def start(bot, update):
    phrases = ['Хорошо, можем продолжить беседу!', 'Хотелось бы пообщаться с ним лично']
    markup = keyboard_markup(phrases)

    if len(User.query.filter_by(telegram_id=update.message.from_user.id).all()) < 1:
        print(update.message.from_user)
        user = User(data=update.message.from_user)
        db.session.add(user)
        db.session.commit()
        print('User has added into the database.')

    bot.send_message(chat_id=update.message.chat_id, text='Привет! Я бот-секретарь, созданный @yuraist. '
                              'Сейчас он немного занят, поэтому ты можешь пообщаться со мной. '
                              'Я передам ему всю важную информацию.', reply_markup=markup)


def hello(bot, update):
    user = update.message.from_user
    update.message.reply_text('Привет, {}'.format(user.first_name))


def incoming_message(bot, update):
    # Message text
    msg = update.message.text
    # Chat id
    chat = update.message.chat_id

    if msg == 'Хорошо, можем продолжить беседу!':
        phrases = ['Да', 'Нет, у меня уже есть']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Отлично! Скажи, тебе нужен свой сайт, мобильное приложение или бот?',
                         reply_markup=markup)
    elif msg == 'Хотелось бы пообщаться с ним лично' or msg == 'Связаться с разработчиком':
        phrases = ['Посмотреть список услуг', 'Связаться с разработчиком']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Тогда ты можешь связаться с ним, написав лично в Telegram: @yuraist. '
                                    'Либо же можете поговорить с ним в VK: vk.com/yuraist; '
                                    'Facebook: fb.com/yuraistom; Email: yura.ist@icloud.com', reply_markup=markup)
    elif msg == 'Да':
        phrases = ['Мне нужен сайт 👨‍💻',
                   'iOS-приложение 📱',
                   'Хочу бота для Telegram 🤖',
                   'А что, Android-приложений нет? 🤔']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Мой создатель может взять эту работу на себя. '
                                    'Что именно тебе необходимо разработать?',
                         reply_markup=markup)
    elif msg == 'Мне нужен сайт 👨‍💻':
        phrases = ['Оставить комментарий', 'Отменить']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Отлично, тогда я оформлю заказ, '
                                    'а ты можешь оставить комментарий кратким описанием сайта. '
                                    'После оформления заказа тебе напишет мой разработчик, '
                                    'и вы сможете обсудить все детали. Окей?', reply_markup=markup)
    elif msg == 'iOS-приложение 📱':
        phrases = ['Оставить комментарий', 'Отменить']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Отлично, тогда я оформлю заказ, '
                                    'а ты можешь оставить комментарий кратким описанием своего приложения. '
                                    'После оформления заказа тебе напишет мой разработчик, '
                                    'и вы сможете обсудить все детали. Окей?', reply_markup=markup)
    elif msg == 'Хочу бота для Telegram 🤖':
        phrases = ['Оставить комментарий', 'Отменить']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Отлично, тогда я оформлю заказ, '
                                    'а ты можешь оставить комментарий кратким описанием бота. '
                                    'После оформления заказа тебе напишет мой разработчик, '
                                    'и вы сможете обсудить все детали. Окей?', reply_markup=markup)
    elif msg == 'А что, Android-приложений нет? 🤔':
        phrases = ['Посмотреть список услуг', 'Связаться с разработчиком']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='К сожалению, разработки Android-приложений пока что нет в списке наших услуг.',
                         reply_markup=markup)
    elif msg == 'Посмотреть список услуг':
        phrases = ['Мне нужен сайт 👨‍💻',
                   'iOS-приложение 📱',
                   'Хочу бота для Telegram 🤖',
                   'А что, Android-приложений нет? 🤔']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Мой создатель может разработать для тебя iOS-приложение, '
                                    'сайт или бота для Telegram. Что именно тебя интересует?', reply_markup=markup)
    elif msg == 'Оставить комментарий':
        bot.send_message(chat, text='Чтобы написать комментарий, воспользуйся командой /app, '
                                    'если тебе нужно приложение, /website, если требуется создать сайт, '
                                    'или /bot, если нужно разработать бота. Просто напиши текст сообщения после '
                                    'команды (Пример сообщения: "/bot Хочу бота, который будет принимать заказы от '
                                    'моих покупателей"), а я занесу твой заказ в базу данных.')
    elif msg == 'Отменить' or msg == 'Нет, у меня уже есть':
        text = 'Ладно. Если захочешь еще раз посмотреть список наших предложений, то просто напиши ' \
               '«Посмотреть список услуг» или вызови команду /goods_list'
        bot.send_message(chat, text)
    else:
        phrases = ['Посмотреть список услуг', 'Связаться с разработчиком']
        markup = keyboard_markup(phrases)
        bot.send_message(chat, text='Извини, но я еще не знаю, как правильно отвечать на такие сообщения. '
                         'Лучше воспользуйся готовыми командами.', reply_markup=markup)

def goods_list(bot, update):
    chat = update.message.chat_id
    phrases = ['Мне нужен сайт 👨‍💻',
               'iOS-приложение 📱',
               'Хочу бота для Telegram 🤖',
               'А что, Android-приложений нет? 🤔']
    markup = keyboard_markup(phrases)
    bot.send_message(chat, text='Мой создатель может разработать для тебя iOS-приложение, '
                                'сайт или бота для Telegram. Что именно тебя интересует?', reply_markup=markup)


def app(bot, update):
    chat = update.message.chat_id
    phrases = ['Посмотреть список услуг', 'Связаться с разработчиком']
    markup = keyboard_markup(phrases)

    order = Order()
    order.user_id = User.query.filter_by(telegram_id=update.message.from_user.id).first().id
    order.comment = update.message.text
    order.type = 'app'

    db.session.add(order)
    db.session.commit()

    bot.send_message(chat, text='Отлично. Я создал запрос. В скором времени с тобой свяжется разработчик. '
                                'Было приятно пообщаться!', reply_markup=markup)


def tg_bot(bot, update):
    print(update.message.text)
    chat = update.message.chat_id
    phrases = ['Посмотреть список услуг', 'Связаться с разработчиком']
    markup = keyboard_markup(phrases)

    order = Order()
    order.user_id = User.query.filter_by(telegram_id=update.message.from_user.id).first().id
    order.comment = update.message.text
    order.type = 'bot'

    db.session.add(order)
    db.session.commit()

    bot.send_message(chat, text='Отлично. Я создал запрос. В скором времени с тобой свяжется разработчик. '
                                'Было приятно пообщаться!', reply_markup=markup)


def website(bot, update):
    chat = update.message.chat_id
    phrases = ['Посмотреть список услуг', 'Связаться с разработчиком']
    markup = keyboard_markup(phrases)

    order = Order()
    order.user_id = User.query.filter_by(telegram_id=update.message.from_user.id).first().id
    order.comment = update.message.text
    order.type = 'website'

    db.session.add(order)
    db.session.commit()

    bot.send_message(chat, text='Отлично. Я создал запрос. В скором времени с тобой свяжется разработчик. '
                                'Было приятно пообщаться!', reply_markup=markup)


def error(bot, update, error):
    logger.warning('Update "{}" caused error "{}"'.format(update, error))


def main():
    updater = Updater(token=os.environ['TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler('goods_list', goods_list))
    dispatcher.add_handler(CommandHandler('app', app))
    dispatcher.add_handler(CommandHandler('website', website))
    dispatcher.add_handler(CommandHandler('bot', tg_bot))
    dispatcher.add_handler(MessageHandler(Filters.text, incoming_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
