from . import main
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

@main.route('/')
def index():
    if not current_user.is_authenticated:
        flash("您必须先注册才能记账。")
        return redirect(url_for('auth.login'))
    return render_template('index.html')