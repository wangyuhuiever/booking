#! -*- encoding:utf-8 -*-
from . import main
from flask import render_template, redirect, url_for, request, current_app, flash
from flask_login import current_user, login_required
from .forms import DataForm, ModifyDataForm, AddOutlayForm
from ..models import Record, Outlay
from .. import db
from datetime import date, timedelta

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.confirmed:
        return redirect(url_for('auth.unconfirmed'))
    form = DataForm()
    if form.validate_on_submit():
        record = Record(timestamp=form.timestamp.data,
                        number=form.number.data,
                        message=form.message.data,
                        money=form.money.data,
                        leixing=form.leixing.data,
                        outlay=Outlay.query.get(form.outlay.data),
                        own=current_user._get_current_object())
        db.session.add(record)
        return redirect(url_for('main.index'))
    records = current_user.records.order_by(Record.id.desc()).all()
    counts = len(records)
    return render_template('index.html', form=form, records=records[:5],
                           counts=counts)

@main.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify(id):
    record = Record.query.get_or_404(id)
    form = ModifyDataForm(record)
    if form.validate_on_submit():
        record.timestamp = form.timestamp.data
        record.number = form.number.data
        record.message = form.message.data
        record.money = form.money.data
        record.leixing = form.leixing.data
        record.outlay = Outlay.query.get(form.outlay.data)
        record.delete = form.delete.data
        if record.delete == True:
            db.session.delete(record)
        else:
            db.session.add(record)
        return redirect(url_for('main.index'))
    form.timestamp.data = record.timestamp
    form.number.data = record.number
    form.message.data = record.message
    form.money.data = record.money
    form.leixing.data = record.leixing
    form.outlay.data = record.outlay
    form.delete.data = record.delete
    return render_template('modify.html', form=form, record=record)

@main.route('/addoutlay', methods=['GET', 'POST'])
@login_required
def addoutlay():
    form = AddOutlayForm()
    outlays = Outlay.query.all()
    outlay_list = []
    for outlay in outlays:
        outlay_list.append(outlay.name)
    if form.validate_on_submit():
        addname = form.name1.data + '--' + form.name2.data
        if addname in outlay_list:
            flash('该科目已存在')
        else:
            o = Outlay(name=addname)
            db.session.add(o)
            flash('添加成功')
        return redirect(url_for('main.addoutlay'))
    return render_template('addoutlay.html', form=form, outlay_list=outlay_list)

@main.route('/deleteoutlay', methods=['GET', 'POST'])
@login_required
def deleteoutlay():
    outlays = Outlay.query.order_by(Outlay.name.asc())
    outlay_list = []
    for outlay in outlays:
        if outlay.id != 1:
            outlay_list.append(outlay.name)
    form = AddOutlayForm()
    if form.validate_on_submit():
        deletename = form.name1.data + '--' + form.name2.data
        o = Outlay.query.filter_by(name=deletename).first()
        if deletename in outlay_list:
            db.session.delete(o)
            flash('删除成功')
        else:
            flash('没有此科目')
        return redirect(url_for('main.deleteoutlay'))
    return render_template('deleteoutlay.html', form=form, outlay_list=outlay_list)

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

@main.route('/index/leixing/<string:leixing>/<string:timestamp>')
@login_required
def leixing(leixing, timestamp):
    begin_time = date(int(timestamp[:4]), int(timestamp[5:7]), 1)
    end_time = date(int(timestamp[:4]), int(timestamp[5:7]) + 1, 1) - timedelta(1)
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.filter_by(leixing=leixing).\
        filter(Record.timestamp.between(begin_time, end_time)).order_by(Record.id.desc()).paginate(
        page, per_page=current_app.config['SHOW_IN_QUERY'],
        error_out=False)
    records = pagination.items
    return render_template('leixing.html', pagination=pagination, records=records,
                           leixing=leixing)

@main.route('/index/timestamp/<string:timestamp>')
@login_required
def timestamp(timestamp):
    begin_time = date(int(timestamp[:4]), int(timestamp[5:7]), 1)
    end_time = date(int(timestamp[:4]), int(timestamp[5:7])+1, 1) - timedelta(1)
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.filter(Record.timestamp.between(begin_time, end_time))\
        .order_by(Record.id.desc()).paginate(
        page, per_page=current_app.config['SHOW_IN_QUERY'],
        error_out=False)
    records = pagination.items
    return render_template('timestamp.html', pagination=pagination, records=records,
                           leixing='月份')

@main.route('/index/outlay/<string:outlay>/<string:timestamp>')
@login_required
def outlay(outlay, timestamp):
    yiji = outlay[:outlay.find('--')]
    kemu = Outlay.query.filter(Outlay.name.startswith(yiji)).all()
    begin_time = date(int(timestamp[:4]), int(timestamp[5:7]), 1)
    end_time = date(int(timestamp[:4]), int(timestamp[5:7]) + 1, 1) - timedelta(1)
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.join(Outlay, Outlay.name.startswith(yiji)). \
        filter(Record.timestamp.between(begin_time, end_time)).order_by(Record.id.desc()).paginate(
        page, per_page=current_app.config['SHOW_IN_QUERY'],
        error_out=False)
    records = pagination.items
    return render_template('outlay.html', records=records, pagination=pagination,
                           leixing='科目')

@main.route('/index/fulloutlay/<string:outlay>/<string:timestamp>')
@login_required
def fulloutlay(outlay, timestamp):
    begin_time = date(int(timestamp[:4]), int(timestamp[5:7]), 1)
    end_time = date(int(timestamp[:4]), int(timestamp[5:7]) + 1, 1) - timedelta(1)
    page = request.args.get('page', 1, type=int)
    pagination = current_user.records.filter(Record.outlay_id==outlay) \
        .filter(Record.timestamp.between(begin_time, end_time)).order_by(Record.id.desc()).paginate(
        page, per_page=current_app.config['SHOW_IN_QUERY'],
        error_out=False)
    records = pagination.items
    return render_template('outlay.html', pagination=pagination, records=records,
                           leixing='二级科目')

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
