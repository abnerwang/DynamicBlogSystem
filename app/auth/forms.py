from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from ..models import User


class UserRegisterForm(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired(), Length(min=9, max=10, message='学号格式不正确！')])
    username = StringField('用户名', validators=[DataRequired(), Length(min=1, max=64, message='用户名长度为 1 到 64 位！')])
    email = StringField('电子邮件地址', validators=[DataRequired(), Email(message='必须是有效的 Email 地址！')])
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


class UserLoginForm(FlaskForm):
    email = StringField('电子邮件地址', validators=[DataRequired(), Email(message='必须是有效的 Email 地址！')])
    password = StringField('密码', validators=[DataRequired(message='密码不能为空！')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_email(self, field):
        user = User.query.filter_by(email_address=field.data).first()
        if user is None:
            raise ValidationError('您所输入的电子邮件地址尚未注册！')


class ChangePwdForm(FlaskForm):
    old_password = StringField('旧密码', validators=[DataRequired()])
    password = StringField('新密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致！'),
                                              Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',
                                                     message='密码必须同时含有字母、数字和特殊字符，且不能低于 8 位！')])
    password2 = StringField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('确认修改')
