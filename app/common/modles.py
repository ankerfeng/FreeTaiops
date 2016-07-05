#!/usr/bin/env python
#coding:utf-8

import random
import string
import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import  generate_password_hash, check_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
mysql_engine = create_engine('mysql://root:taiops@localhost:3306/taiops?charset=utf8', pool_recycle=100)
Session = sessionmaker(bind=mysql_engine)
session = Session()


# 项目表
class ProjectModel(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225))
    rootdomain = db.Column(db.String(225))
    note = db.Column(db.String(225))
    uid = db.Column(db.Integer)
    utime = db.Column(db.DateTime)

    def __repr__(self):
        return 'target %r' % self.name

# 项目域名表
class ProjectDomainModel(db.Model):
    __tablename__ = 'project_domain'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    domain = db.Column(db.String(225))
    utime = db.Column(db.DateTime)
    note = db.Column(db.String(225))
    uid = db.Column(db.Integer)
    def __repr__(self):
        return 'domain %r' % self.domain

#项目网站表
class ProjectSiteModel(db.Model):
    __tablename__ = 'project_site'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    url = db.Column(db.String(225))
    utime = db.Column(db.DateTime)
    note = db.Column(db.String(225))
    uid = db.Column(db.Integer)
    def __repr__(self):
        return 'domain %r' % self.domain

#项目IP表
class ProjectIpModel(db.Model):

    __tablename__ = 'project_ip'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    ip = db.Column(db.String(225))
    utime = db.Column(db.DateTime)
    note = db.Column(db.String(225))

    def __repr__(self):
        return 'ip %r' % self.ip

#资产导入记录表
class AssertAddLogModel(db.Model):
    __tablename__ = 'assert_add_log'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    value = db.Column(db.String(225))
    type = db.Column(db.String(225))
    note = db.Column(db.String(225))
    addtime = db.Column(db.DateTime)


#IP端口表
class IpPortModel(db.Model):
    __tablename__ = 'ipport'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(225))
    port = db.Column(db.String(225))
    protocol = db.Column(db.String(225))
    utime = db.Column(db.DateTime)

    def __repr__(self):
        return 'ip: %r' % self.ip

#Dns数据表
class DnsModel(db.Model):
    __tablename__ = 'dns'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(225))
    ip = db.Column(db.String(225))
    cname = db.Column(db.String(225))
    nstype = db.Column(db.String(225))
    udate = db.Column(db.Date())

    def __repr__(self):
        return 'host: %r' % self.host

#站点信息表
class SiteModel(db.Model):

    __tablename__ = 'site'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(225))
    title = db.Column(db.String(225))
    code = db.Column(db.Integer)
    app = db.Column(db.String(255))
    utime = db.Column(db.DateTime)

    def __repr__(self):
        return '<site %s>' % self.host

#任务记录表
class TaskModel(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    taskname = db.Column(db.String(225))
    args = db.Column(db.String(225))
    status = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)


#用户表
class UserModel(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225))
    pwdhash = db.Column(db.String(225))
    email = db.Column(db.String(225))
    nick = db.Column(db.String(225))
    apikey = db.Column(db.String(225))

    @property
    def password(self):
        raise AttributeError('password is not readable attribuye')

    @password.setter
    def password(self, password):
        self.pwdhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def produce_key(self):
        key =  ''.join(random.sample(string.ascii_letters+string.digits, 8))+"-"+''.join(random.sample(string.ascii_letters+string.digits, 8))+ \
        "-"+''.join(random.sample(string.ascii_letters + string.digits, 8))+"-"+''.join(random.sample(string.ascii_letters+string.digits, 8))
        print key

    def __repr__(self):
        return '<name %s>' % self.name

#登录记录表
class UserLoginInfoModel(db.Model):
    __tablename__ = 'user_login_info'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    ltime = db.Column(db.DateTime)
    ip = db.Column(db.String(225))




