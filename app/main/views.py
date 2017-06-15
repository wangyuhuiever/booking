from . import main
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from .forms import DataForm
from ..models import Record, Leixing
from .. import db

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.confirmed:
        return redirect(url_for('auth.unconfirmed'))
    return render_template('index.html')

@main.route('/jizhang', methods=['GET', 'POST'])
@login_required
def jizhang():
    record = Record.generate_instance()
    form = DataForm(record)
    if form.validate_on_submit():
        record.number=form.number.data
        record.leixing=Leixing.query.get(form.leixing.data)
        record.message=form.message.data
        record.own=current_user._get_current_object()
        db.session.add(record)
        return redirect(url_for('main.jizhang'))
    else:
        db.session.delete(record)
    return render_template('jizhang.html', form=form)