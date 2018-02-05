from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from ..models import User


class UserRegisterForm(FlaskForm):
    student_id = StringField('学号',
                             validators=[DataRequired(message='学号不能为空！'), Length(min=9, max=10, message='学号格式不正确！')])
    username = StringField('姓名', validators=[DataRequired(message='姓名不能为空！'),
                                             Length(min=1, max=64, message='用户名长度为 1 到 64 位！')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空！'), Email(message='必须是有效的邮箱地址！')])
    password = StringField('密码',
                           validators=[DataRequired(message='密码不能为空！'), EqualTo('password2', message='两次输入的密码不一致！'),
                                       Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',
                                              message='密码必须同时含有字母、数字和特殊字符，且不能低于 8 位！')])
    password2 = StringField('确认密码', validators=[DataRequired(message='确认密码不能为空！')])
    submit = SubmitField('注册')

    def validate_student_id(self, field):
        if User.query.filter_by(student_id=field.data).first():
            raise ValidationError('该学号已注册！')

    def validate_email(self, field):
        if User.query.filter_by(email_address=field.data).first():
            raise ValidationError('该邮箱已注册！')


class UserLoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空！'), Email(message='必须是有效的邮箱地址！')])
    password = StringField('密码', validators=[DataRequired(message='密码不能为空！')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class ChangePwdForm(FlaskForm):
    old_password = StringField('旧密码', validators=[DataRequired(message='请输入旧密码！')])
    password = StringField('新密码',
                           validators=[DataRequired(message='密码不能为空！'), EqualTo('password2', message='两次输入的密码不一致！'),
                                       Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',
                                              message='密码必须同时含有字母、数字和特殊字符，且不能低于 8 位！')])
    password2 = StringField('确认新密码', validators=[DataRequired(message='确认密码不能为空！')])
    submit = SubmitField('确认修改')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空！'), Email(message='请输入有效的邮箱地址！')])
    submit = SubmitField('提交')


class ResetPasswordForm(FlaskForm):
    password = StringField('新密码',
                           validators=[DataRequired(message='密码不能为空！'), EqualTo('password2', message='两次输入的密码不一致！'),
                                       Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',
                                              message='密码必须同时含有字母、数字和特殊字符，且不能低于 8 位！')])
    password2 = StringField('确认新密码', validators=[DataRequired(message='确认密码不能为空！')])
    submit = SubmitField('确认')
