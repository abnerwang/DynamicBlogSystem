from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..models import User


class UserRegisterForm(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired(), Length(min=9, max=10)])
    username = StringField('用户名', validators=[DataRequired(), Length(min=5, max=64)])
    email = StringField('电子邮件地址', validators=[DataRequired(), Email()])
    password = StringField('密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致！')])
    password2 = StringField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_student_id(self):
        if User.query.filter_by(student_id=self.student_id).first():
            raise ValidationError('该学号已注册！')

    def validate_username(self):
        if User.query.filter_by(username=self.username).first():
            raise ValidationError('用户名已存在！')

    def validate_email(self):
        if User.query.filter_by(email_address=self.email).first():
            raise ValidationError('该电子邮件已注册！')
