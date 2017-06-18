#! -*- encoding:utf-8 -*-
from ..models import User
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp, ValidationError

class RegistrationForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(message='登录账号'), Length(1, 64), Email()])
    username = StringField("用户名", validators=[Required(), Length(1, 64),
                                              Regexp('\w*$',0,
                                                     '用户名只能包含汉字，字母，数字和下划线')])
    password = PasswordField("密码", validators=[Required(), Length(4, 16,'长度必须在4-16位')])
    password2 = PasswordField("确认密码", validators=[Required(), EqualTo('password','两次密码必须一致')])
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class LoginForm(FlaskForm):
    email = StringField('账号', validators=[Required(message='邮箱地址'), Length(1, 64),Email()])
    password = PasswordField('密码',validators=[Required(), Length(4, 16,'长度在4-16位之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField("登录")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[Required(), Length(4, 16, '长度在4-16位之间')])
    new_password = PasswordField('新密码', validators=[Required(), Length(4, 16, '长度在4-16位之间')])
    new_password2 = PasswordField('确认新密码', validators=[Required(), Length(4, 16, '长度在4-16位之间'),
                                                       EqualTo('new_password', '两次密码必须一致')])
    submit = SubmitField('确认修改')

class PasswordResetRequestForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(message='登录账号'), Length(1, 64), Email()])
    submit = SubmitField("提交")

class PasswordResetForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(message='登录账号'), Length(1, 64), Email()])
    password = PasswordField("密码", validators=[Required(), Length(4, 16, '长度必须在4-16位')])
    password2 = PasswordField("确认密码", validators=[Required(), EqualTo('password', '两次密码必须一致')])
    submit = SubmitField("确认修改")

    def validate_email(self, field):
        if User.query.filter_by(email= field.data).first() is None:
            raise ValidationError('该邮箱未注册')