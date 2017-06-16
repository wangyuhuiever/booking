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
    records = current_user.records.order_by(Record.id.desc()).all()
    counts = len(records)
    return render_template('index.html', form=form, records=records[:5],
                           counts=counts)

@main.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    record = Record.query.get_or_404(id)
    form = ChangeDataForm(record)
    if form.validate_on_submit():
        record.number=form.number.data
        record.leixing=form.leixing.data
        record.message=form.message.data
        record.delete=form.delete.data
        if record.delete == True:
            db.session.delete(record)
        else:
            db.session.add(record)
        return redirect(url_for('main.index'))
    form.number.data = record.number
    form.leixing.data = record.leixing
    form.message.data = record.message
    form.delete.data = record.delete
    return render_template('change.html', form=form, record=record)

@main.route('/all')
@login_required
def all():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.order_by(Record.id.desc()).paginate(
        page, per_page=current_app.config['SHOW_IN_QUERY'],
        error_out=False)
    records = pagination.items
    return render_template('all.html', pagination=pagination,
                           records=records)

@main.route('/index/leixing/<string:leixing>')
@login_required
def leixing(leixing):
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.filter_by(leixing=leixing).order_by(Record.timestamp).paginate(
        page, per_page=current_app.config['SHOW_IN_QUERY'],
        error_out=False)
    records = pagination.items
    return render_template('leixing.html', pagination=pagination, records=records,
                           leixing=leixing)

@main.route('/report')
@login_required
def report():
    records = current_user.records
    income = 0
    expenditure = 0
    for record in records:
        if record.leixing == '支出':
            expenditure += record.number
        else:
            income += record.number
    return render_template('report.html', income=income, expenditure=expenditure)