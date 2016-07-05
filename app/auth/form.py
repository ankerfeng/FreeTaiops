#!/usr/bin/env python
#coding:utf8

import os
import sys
sys.path.append(os.path.abspath("./../"))

from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp
from app.common.modles import UserModel


class LoginForm(Form):
    #登录表单
    email = StringField('邮箱', validators=[DataRequired(message="邮箱不能为空"), Length(1, 64),
                                          Email(message="邮箱格式不正确")])
    password = PasswordField('密码', validators=[DataRequired(message="密码不能为空")])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class PwdForm(Form):
    #密码修改表单
    old_password = PasswordField('旧密码', validators=[DataRequired(message="旧密码不能为空")])

    newpwd = PasswordField('密码', validators=[
        DataRequired(message="密码不能为空"), EqualTo('newpwd2', message='两次输入的密码不一致！')])

    newpwd2 = PasswordField('确认密码', validators=[DataRequired(message="确认密码不能为空")])
    submit = SubmitField('修改')

    def validate_old_password(self, field):
        if not current_user.verify_password(self.old_password.data):
            raise ValidationError(message='旧密码不正确')

class RegisterForm(Form):
    #注册表单
    email = StringField('邮箱', validators=[DataRequired(message="邮箱不能为空"), Length(1, 64),
                                           Email(message="邮箱格式不正确")])
    username = StringField('用户名', validators=[
        DataRequired(message="用户名不能为空"), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message='用户名格式不正确')])
    password = PasswordField('密码', validators=[
        DataRequired(message="密码不能为空"), EqualTo('password2', message='两次输入的密码不一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired(message="确认密码不能为空")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')