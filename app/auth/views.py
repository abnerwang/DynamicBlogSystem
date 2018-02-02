from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import UserRegisterForm, UserLoginForm, ChangePwdForm
from .. import db
from ..email import send_email
from ..models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[
                                                                        :5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, student_id=form.student_id.data, email_address=form.email.data,
                    password=form.password.data)
        db.session.add(user)

        token = user.generate_confirmation_token(expiration=3600)
        send_email(user.email_address, '确认你的账户', 'auth/email/confirm', user=user, token=token)
        flash('注册成功，你现在可以登录了！系统已向你的电子邮件地址发送了一封确认邮件，请于 1 小时内确认账户！')
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


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required  # 登录后才能确认账户
def confirm(token):
    if current_user.confirmed:
        flash('你的账户已经确认过了！')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经成功确认了账户，谢谢！')
    else:
        flash('链接过期或无效，请前往用户资料页重新发送确认邮件！')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html', user=current_user)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token(expiration=3600)
    send_email(current_user.email_address, '确认你的账户', 'auth/email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已发送至你的邮箱，请及时前往确认！')
    return redirect(url_for('main.index'))


@auth.route('/changePwd', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePwdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.change_password(form.password.data)
            flash('你已成功更改了密码！')
        else:
            flash('你所输入的旧密码不正确！')

    return render_template('auth/changePwd.html', form=form)
