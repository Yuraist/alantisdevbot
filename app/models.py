from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    is_bot = db.Column(db.Boolean)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String, unique=True)
    language_code = db.Column(db.String)

    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def __init__(self, data):
        self.telegram_id = data['id']
        self.is_bot = data['is_bot']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.language_code = data['language_code']

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Order #{} type: {}>'.format(self.id, self.type)
