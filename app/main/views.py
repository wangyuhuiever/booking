from . import main
from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from .forms import DataForm, ChangeDataForm
from ..models import Record
from .. import db

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.confirmed:
        return redirect(url_for('auth.unconfirmed'))
    form = DataForm()
    if form.validate_on_submit():
        record = Record(number=form.number.data,
                        leixing=form.leixing.data,
                        message=form.message.data,
                        own=current_user._get_current_object())
        db.session.add(record)
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.order_by(Record.timestamp.desc()).paginate(
        page, per_page=current_app.config['SHOW_IN_INDEX'],
        error_out=False)
    records = pagination.items
    return render_template('index.html', form=form, pagination=pagination,
                           records=records)

@main.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    record = Record.query.get_or_404(id)
    form = ChangeDataForm(record)
    if form.validate_on_submit():
        record.number=form.number.data
        record.leixing=form.leixing.data
        record.message=form.message.data
        db.session.add(record)
        return redirect(url_for('main.index'))
    form.number.data = record.number
    form.leixing.data = record.leixing
    form.message.data = record.message
    return render_template('change.html', form=form)