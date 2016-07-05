#!/usr/bin/env python
#coding:utf8
import os
import sys
sys.path.append(os.path.abspath("./../../"))

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from datetime import datetime

from inc import auth
from form import LoginForm, RegisterForm, PwdForm
from app.server import db
from app.common.modles import UserModel, UserLoginInfoModel
from app.common.form import flash_errors

@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data) #记录登录IP和时间
            db.session.add(UserLoginInfoModel(uid=current_user.id, ip=request.remote_addr, ltime=datetime.now()))
            db.session.commit()
            return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)

    return render_template('/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit() and form.password.data == form.password2.data:
        user = UserModel(email=form.email.data,
                         name=form.username.data,
                         password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect(url_for('auth.login'))
    else:
        flash_errors(form)
    return render_template('/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功')
    return redirect(url_for('auth.login'))


@auth.route('/', methods=["GET", "POST"])
@login_required
def user():
    uli = UserLoginInfoModel.query.filter(UserLoginInfoModel.uid == current_user.id).order_by(UserLoginInfoModel.ltime.desc()).limit(10)
    form = PwdForm()
    if request.method =='POST':
        if form.validate_on_submit():
            user = UserModel.query.filter_by(id=current_user.id).first()
            user.password=form.newpwd2.data
            db.session.add(user)
            db.session.commit()
            logout_user()
            flash('修改成功，请重新登录。')
            return redirect(url_for("auth.login"))
        else:
            flash_errors(form)
    return render_template("users.html", tables = uli, form=form)







