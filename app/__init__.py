import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from bot.bot import main
from app import models

main()


@app.route('/')
def index():
    return 'Hello, I am @AlantisDevBot. Talk with me in the Telegram app.'
