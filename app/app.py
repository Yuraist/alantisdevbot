from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from bot.bot import updater

updater.start_polling()
updater.idle()

@app.route('/')
def index():
    return 'Hello, I am @AlantisDevBot. Talk with me in the Telegram app.'
