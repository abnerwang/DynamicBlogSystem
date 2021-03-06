from flask import render_template, flash, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import JSONWebSignatureSerializer as Serializer

from . import auth
from .forms import UserRegisterForm, UserLoginForm, ChangePwdForm, ResetPasswordRequestForm, ResetPasswordForm
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
        db.session.commit()

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
        if user is None:
            flash('该邮箱尚未注册此系统！')
            return render_template('auth/login.html', form=form)
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
def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        id = data.get('confirm')
        user = User.query.filter_by(id=id).first()
        if user is None:
            flash('用户不存在！')
            return redirect(url_for('main.index'))
        if user.confirmed:
            flash('你的账户已经确认过了！')
            return redirect(url_for('main.index'))
        if user.confirm(token):
            flash('你已经成功确认了账户，谢谢！')
        else:
            flash('链接过期或无效，请前往用户资料页重新发送确认邮件！')
    except:
        flash('链接无效，请前往用户资料页发送确认邮件！')
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
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('成功修改了密码！')
        else:
            flash('你所输入的旧密码不正确！')

    return render_template('auth/changePwd.html', form=form)


@auth.route('/resetPwdViaEmail', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email_address=email).first()
        if user is None:
            flash('你输入的邮箱尚未注册！')
            return render_template('auth/resetPwdViaEmail.html', form=form)
        else:
            token = user.generate_reset_token(expiration=3600)
            send_email(user.email_address, '重设密码', 'auth/email/resetPwd', user=user, token=token,
                       next=request.args.get('next'))
            flash('一封用于重设密码的邮件已发送至你的邮箱！')
            form.email.data = ''
    return render_template('auth/resetPwdViaEmail.html', form=form)


@auth.route('/resetPwd/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            student_id = data.get('student_id')
            user = User.query.filter_by(student_id=student_id).first()
            user.password = form.password.data
            db.session.add(user)
            flash('你的密码已重设，现在可以使用新密码登录了！')
            return redirect(url_for('auth.login'))
        except:
            flash('链接过期或无效！')
            return redirect(url_for('main.index'))
    return render_template('auth/resetPassword.html', form=form)
