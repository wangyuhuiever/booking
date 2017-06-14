from ..models import User
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp, ValidationError

class RegistrationForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(message='登录账号'), Length(1, 64), Email()])
    username = StringField("用户名", validators=[Required(), Length(1, 64),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                     '用户名只能包含字母，数字，小数点和下划线，'
                                                     '必须以字母开头')])
    password = PasswordField("密码", validators=[Required(), Length(4, 16,'长度必须在4-16位')])
    password2 = PasswordField("确认密码", validators=[Required(), EqualTo('password','两次密码必须一致')])
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱以被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class LoginForm(FlaskForm):
    email = StringField('账号', validators=[Required(message='邮箱地址'), Length(1, 64),Email()])
    password = PasswordField('密码',validators=[Required(), Length(4, 16,'长度在4-16位之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField("登录")