#! -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateField
from wtforms.validators import Required, Length, Regexp, ValidationError
from ..models import Outlay

class DataForm(FlaskForm):
    timestamp = DateField("年月日", validators=[Required()])
    number = StringField("凭证号", validators=[Required(), Length(0, 4, '最大位数为4'), Regexp('^[1-9][0-9]*$',0,
                                                                             '凭证号必须为正整数')])
    message = StringField("摘要")
    money = StringField("金额", validators=[Required(), Length(0, 8, '最大位数为8'), Regexp('^[1-9][0-9]*$', 0,
                                                                                       '金额必须为正整数')])
    leixing = SelectField("借贷", choices=[(None, '请选择'), ('支出', '支出'), ('收入', '收入')])
    outlay = SelectField("支出类型", coerce=int, default=True)
    submit = SubmitField("记账")

    def __init__(self, *args, **kwargs):
        super(DataForm, self).__init__(*args, **kwargs)
        self.outlay.choices = [(outlay.id, outlay.name)
                               for outlay in Outlay.query.order_by(Outlay.name).all()]

    def validate_outlay(self, field):
        if field.data == 1:
            raise ValidationError('请选择科目')

class ModifyDataForm(FlaskForm):
    timestamp = DateField("年月日", validators=[Required()])
    number = StringField("凭证号", validators=[Required(), Length(0, 4, '最大位数为4'), Regexp('^[1-9][0-9]*$', 0,
                                                                                       '凭证号必须为正整数')])
    message = StringField("摘要")
    money = StringField("金额", validators=[Required(), Length(0, 8, '最大位数为8'), Regexp('^[1-9][0-9]*$', 0,
                                                                                      '金额必须为正整数')])
    leixing = SelectField("借贷", choices=[(None, '请选择'), ('支出', '支出'), ('收入', '收入')])
    outlay = SelectField("支出类型", coerce=int, default=True)
    delete = BooleanField("删除")
    submit = SubmitField("记账")

    def __init__(self, record, *args, **kwargs):
        super(ModifyDataForm, self).__init__(*args, **kwargs)
        self.outlay.choices = [(outlay.id, outlay.name)
                               for outlay in Outlay.query.order_by(Outlay.name).all()]
        self.record = record

    def validate_outlay(self, field):
        if field.data == 1:
            raise ValidationError('请选择科目')

class AddOutlayForm(FlaskForm):
    name1 = StringField('一级科目', validators=[Required()])
    name2 = StringField('二级科目', validators=[Required()])
    submit = SubmitField('确认')