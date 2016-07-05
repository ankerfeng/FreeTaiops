#!/usr/bin/env python
#coding:utf8

from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, IPAddress, URL
from wtforms import ValidationError
from flask.ext.wtf import Form
from app.common.formatck import domain_check

class PojForm(Form):
    #项目表单
    name = StringField('项目名称', validators=[Length(0, 225), DataRequired(message="项目名称不能为空")])
    rootdomain = StringField('项目根域名', validators=[Length(0, 225), DataRequired(message="根域名不能为空！")])
    note = StringField('项目备注', validators=[Length(0, 225, message="备注内容过长")])
    submit = SubmitField('Submit')

    def validate_rootdomain(self, field):
        if not domain_check(self.rootdomain.data):
            raise ValidationError('域名格式不正确')

class DelPojForm(Form):
    #删除项目
    pid = IntegerField('项目ID', validators=[DataRequired(message="项目不存在")])
    submit = SubmitField('Submit')

class AssetForm(Form):

    domain = StringField('domain', validators=[Length(0, 225), DataRequired(message="域名不能为空")])
    note = StringField('note')
    submit = SubmitField('Submit')

    def validate_domain(self, field):
        if not domain_check(self.domain.data):
            raise ValidationError('域名格式不正确')


class SiteForm(Form):

    url = StringField('url', validators=[Length(0, 225), DataRequired(message="url不能为空"), URL(require_tld=False, message="错误的URL")])
    note = StringField('note')
    submit = SubmitField('Submit')

class IpForm(Form):

    ip = StringField('IP地址', validators=[Length(0, 225), DataRequired(message="IP 地址不能为空"), IPAddress(message="错误的IP地址")])
    note = StringField('备注')
    submit = SubmitField('Submit')

class IPPortForm(Form):

    target = StringField('IP地址', validators=[Length(0, 225), DataRequired(message="IP不能为空 地址不能为空"), IPAddress(message="非法的IP地址")])
    port = IntegerField('端口', validators=[DataRequired(message="项目不存在"), NumberRange(min=0, max=65535, message="非法的端口")])
    note = StringField('note')
    submit = SubmitField('Submit')

class ProjectDomainForm(Form):

    pid = IntegerField('项目ID', validators=[DataRequired(message="项目不存在")])
    domain = StringField('域名', validators=[DataRequired(message="域名不能为空")])
    note =  StringField('备注')
    submit = SubmitField('添加')

    def validate_domain(self, field):
        if not domain_check(self.domain.data):
            raise ValidationError('域名格式不正确')

class DelProjectDomainForm(Form):

    id = IntegerField('域名ID', validators=[DataRequired(message="域名不存在")])
    pid = IntegerField('项目ID', validators=[DataRequired(message="项目不存在")])
    submit = SubmitField('Submit')

class ProjectSiteForm(Form):

    pid = IntegerField('项目ID', validators=[DataRequired(message="项目不存在")])
    url = StringField('url', validators=[DataRequired(message="域名不能为空"), URL(require_tld=False, message="url格式不正确")])
    note =  StringField('备注')
    submit = SubmitField('添加')

class DelProjectSiteForm(Form):

    id = IntegerField('网站ID', validators=[DataRequired(message="域名不存在")])
    pid = IntegerField('项目ID', validators=[DataRequired(message="项目不存在")])
    submit = SubmitField('Submit')

class ProjectIpForm(Form):

    pid = IntegerField('项目ID', validators=[DataRequired(message="项目不存在")])
    ip = StringField('url', validators=[DataRequired(message="域名不能为空"), IPAddress(message="IP地址格式不正确")])
    note =  StringField('备注')
    submit = SubmitField('添加')





