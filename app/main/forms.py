from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length
from ..models import Leixing

class DataForm(FlaskForm):
    number = StringField("金额", validators=[Required(), Length(0, 8)])
    leixing = SelectField("借贷", coerce=int)
    message = StringField("备注")
    submit = SubmitField("记账")

    def __init__(self, record, *args, **kwargs):
        super(DataForm, self).__init__(*args, **kwargs)
        self.leixing.choices = [(leixing.id, leixing.name)
                                for leixing in Leixing.query.order_by(Leixing.id).all()]
        self.record = record