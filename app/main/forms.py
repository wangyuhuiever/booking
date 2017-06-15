from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length

class DataForm(FlaskForm):
    number = StringField("金额", validators=[Required(), Length(0, 8)])
    leixing = SelectField("借贷", choices=[(None, '请选择'), ('支出', '支出'), ('收入', '收入')])
    message = StringField("备注")
    submit = SubmitField("记账")

class ChangeDataForm(FlaskForm):
    number = StringField("金额", validators=[Required(), Length(0, 8)])
    leixing = SelectField("借贷", choices=[(None, '请选择'), ('支出', '支出'), ('收入', '收入')])
    message = StringField("备注")
    submit = SubmitField("记账")

    def __init__(self,record, *args, **kwargs):
        self.record=record