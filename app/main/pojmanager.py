#!/usr/bin/env python
#coding:utf8

import os
import sys
sys.path.append(os.path.abspath("./../../../"))
from datetime import datetime

from inc import main
from flask import render_template, redirect, request, flash, g as G
from flask.ext.login import current_user, login_required

from form import ProjectDomainForm, DelProjectDomainForm, ProjectSiteForm,DelProjectSiteForm, ProjectIpForm
from app.server import db
from app.common.form import flash_errors, return_errors
from app.common.modles import  ProjectDomainModel, ProjectSiteModel, ProjectIpModel



@main.route('/add_poj_domain', methods=["GET", "POST"])
@login_required
def add_poj_domain():
    '''
    添加项目根域名
    :return:None
    '''
    form = ProjectDomainForm()
    if request.method == "GET":
        return render_template("add_project_domain.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            poj_domain = ProjectDomainModel(pid=form.pid.data, domain=form.domain.data, \
                                                note=form.note.data, utime=datetime.now(), uid=current_user.id)
            db.session.add(poj_domain)
            db.session.commit()

            return "添加成功."
        else:
            msg = ''
            for error in return_errors(form):
                msg += error
            return msg

@main.route('/del_poj_domain', methods=["GET", "POST"])
@login_required
def del_poj_domain():
    '''
    删除项目域名
    :return:msg
    '''
    form = DelProjectDomainForm()
    if request.method == "GET":
        return render_template("/del_project_domain.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            poj_domain = ProjectDomainModel.query.filter(ProjectDomainModel.uid == current_user.id, \
                                                  ProjectDomainModel.pid == form.pid.data, ProjectDomainModel.id == form.id.data).first()
            if poj_domain is not None:
                db.session.delete(poj_domain)
                db.session.commit()
                return "删除成功"
            else:
                return "不存在的域名"
        else:
            msg = ''
            for error in return_errors(form):
                msg += error
            return msg

@main.route('/add_poj_site', methods=["GET", "POST"])
@login_required
def add_poj_site():
    '''
    添加项目网站
    :return:None
    '''
    form = ProjectSiteForm()
    if request.method == "GET":
        return render_template("add_project_site.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            poj_site = ProjectSiteModel(pid=form.pid.data, url=form.url.data, note=form.note.data,\
                                                utime=datetime.now(), uid=current_user.id)
            db.session.add(poj_site)
            db.session.commit()
            return "添加成功."
        else:
            msg = ''
            for error in return_errors(form):
                msg += error
            return msg

@main.route('/del_poj_site', methods=["GET", "POST"])
@login_required
def del_poj_site():
    '''
    删除项目网站
    :return:msg
    '''
    form = DelProjectSiteForm()
    if request.method == "GET":
        return render_template("/del_project_site.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            poj_site = ProjectSiteModel.query.filter(ProjectSiteModel.uid == current_user.id, \
                                                  ProjectSiteModel.pid == form.pid.data, ProjectSiteModel.id == form.id.data).first()
            if poj_site is not None:
                db.session.delete(poj_site)
                db.session.commit()
                return "删除成功"
            else:
                return "不存在的域名"
        else:
            msg = ''
            for error in return_errors(form):
                msg += error
            return msg

@main.route('/add_poj_ip', methods=["GET", "POST"])
@login_required
def add_poj_ip():
    '''
    添加项目IP
    :return:None
    '''
    form = ProjectIpForm()
    if request.method == "GET":
        return render_template("add_project_ip.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            poj_ip = ProjectIpModel(pid=form.pid.data, ip=form.ip.data, note=form.note.data,\
                                                utime=datetime.now(), uid=current_user.id)
            db.session.add(poj_ip)
            db.session.commit()
            return "添加成功."
        else:
            msg = ''
            for error in return_errors(form):
                msg += error
            return msg

@main.route('/del_poj_ip', methods=["GET", "POST"])
@login_required
def del_poj_ip():
    '''
    删除项目IP
    :return:msg
    '''
    form = DelProjectSiteForm()
    if request.method == "GET":
        return render_template("/del_project_ip.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            poj_site = ProjectIpModel.query.filter(ProjectIpModel.uid == current_user.id, \
                                                  ProjectIpModel.pid == form.pid.data, ProjectIpModel.id == form.id.data).first()
            if poj_site is not None:
                db.session.delete(poj_site)
                db.session.commit()
                return "删除成功"
        else:
            msg = ''
            for error in return_errors(form):
                msg += error
            return msg


