from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required

from . import auth
from .forms import UserRegisterForm, UserLoginForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, student_id=form.student_id.data, email_address=form.email.data,
                    password=form.password.data)
        db.session.add(user)

        flash('注册成功，你现在可以登录了！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email.data).first()
        if user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('密码错误！')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出！')
    return redirect(url_for('main.index'))
