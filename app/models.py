from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
import hashlib

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    records = db.relationship('Record', backref='own', lazy='dynamic')
    avatar_hash = db.Column(db.String(32))

    @property
    def password(self):
        raise AttributeError('密码字段不可读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'http://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def lode_user(user_id):
    return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
    pass
login_manager.anonymous_user = AnonymousUser

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True)
    message = db.Column(db.String, index=True, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    own_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    leixing_id = db.Column(db.Integer, db.ForeignKey('leixings.id'))

    @staticmethod
    def generate_instance():
        count = Record.query.count() + 1
        record = Record(id=count)
        db.session.add(record)
        db.session.commit()
        return record

    def __repr__(self):
        return '<Record %s>' %self.timestamp

class Leixing(db.Model):
    __tablename__ = 'leixings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    records = db.relationship('Record', backref='leixing', lazy='dynamic')
    default = db.Column(db.Boolean, index=True, default=False)
    counts = db.Column(db.Integer)

    @staticmethod
    def insert_leixings():
        leixings = {
            '请选择':(0, True),
            '支出': (-1, False),
            '收入': (1, False)
        }
        for l in leixings:
            leixing = Leixing.query.filter_by(name=l).first()
            if leixing is None:
                leixing = Leixing(name=l)
            leixing.counts = leixings[l][0]
            leixing.default = leixings[l][1]
            db.session.add(leixing)
        db.session.commit()

    def __repr__(self):
        return '<Leixing %r>' % self.name