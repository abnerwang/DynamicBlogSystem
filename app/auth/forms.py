from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from ..models import User


class UserRegisterForm(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired(), Length(min=9, max=10, message='学号格式不正确！')])
    username = StringField('用户名', validators=[DataRequired(), Length(min=1, max=64, message='用户名长度为 1 到 64 位！')])
    email = StringField('电子邮件地址', validators=[DataRequired(), Email()])
    password = StringField('密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致！'),
                                             Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',
                                                    message='密码必须同时含有字母、数字和特殊字符，且不能低于 8 位！')])
    password2 = StringField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_student_id(self, field):
        if User.query.filter_by(student_id=field.data).first():
            raise ValidationError('该学号已注册！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')

    def validate_email(self, field):
        if User.query.filter_by(email_address=field.data).first():
            raise ValidationError('该电子邮件已注册！')
