#! -*- encoding:utf-8 -*-
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User %s>' % self.username

@login_manager.user_loader
def lode_user(user_id):
    return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
    pass
login_manager.anonymous_user = AnonymousUser

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date, index=True)
    number = db.Column(db.Integer, index=True)
    message = db.Column(db.String, index=True)
    money = db.Column(db.Integer, index=True)
    leixing = db.Column(db.String, nullable=False, index=True)
    outlay_id = db.Column(db.Integer, db.ForeignKey('outlays.id'))
    own_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    delete = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)
        if self.outlay is None:
            self.outlay = Outlay.query.filter_by(default=True).first()

    def __repr__(self):
        return '<Record %s>' %self.timestamp

class Outlay(db.Model):
    __tablename__ = 'outlays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    records = db.relationship('Record', backref='outlay', lazy='dynamic')

    @staticmethod
    def insert_outlays():
        outlays = {
            '请选择': ((None,), True),
            '管理费用':(('办公费', '招待费', '人员工资',
                     '修理费', '奖金', '水电费'), False),
            '活动业务成本':(('房租', '教师工资', '宣传费'), False),
            '税金':(('所得税', '增值税', '企业所得税', '印花税',
                   '城建税'), False)
        }
        for o1 in outlays:
            for o2 in outlays[o1][0]:
                if o2 is None:
                    outlay = Outlay.query.filter_by(name=o1).first()
                else:
                    outlay = Outlay.query.filter_by(name=o1 + '--' + o2).first()
                if outlay is None:
                    if o2 is None:
                        outlay = Outlay(name=o1)
                    else:
                        outlay = Outlay(name=o1 + '--' + o2)
                outlay.default = outlays[o1][1]
                db.session.add(outlay)
        db.session.commit()

    def __repr__(self):
        return '<Outlay %s>' % self.name