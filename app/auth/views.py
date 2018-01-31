from flask import render_template, flash

from . import auth
from .forms import UserRegisterForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, student_id=form.student_id.data, email_address=form.email.data)
        db.session.add(user)

        flash('注册成功，你现在可以登录了！')

    return render_template('auth/register.html', form=form)
