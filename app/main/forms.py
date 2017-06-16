#! -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import Required, Length, Regexp

class DataForm(FlaskForm):
    number = StringField("金额", validators=[Required(), Length(0, 8, '最大位数为8'), Regexp('^[1-9][0-9]*$',0,
                                                                             '金额必须为正整数')])
    leixing = SelectField("借贷", choices=[(None, '请选择'), ('支出', '支出'), ('收入', '收入')])
    message = StringField("备注")
    submit = SubmitField("记账")

class ChangeDataForm(FlaskForm):
    number = StringField("金额", validators=[Required(), Length(0, 8, '最大位数为8'), Regexp('^[1-9][0-9]*$',0,
                                                                             '金额必须为正整数')])
    leixing = SelectField("借贷", choices=[(None, '请选择'), ('支出', '支出'), ('收入', '收入')])
    message = StringField("备注")
    delete = BooleanField("删除")
    submit = SubmitField("确认")

    def __init__(self,record, *args, **kwargs):
        super(ChangeDataForm, self).__init__(*args, **kwargs)
        self.record=record
