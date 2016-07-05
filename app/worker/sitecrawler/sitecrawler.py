#!/usr/bin/env python
#coding:utf8
# 网站首页信息

import os
import sys
sys.path.append(os.path.abspath("./../../../"))

import re
import json
import requests
from datetime import datetime

from app.common.modles import SiteModel, Session

class SiteCrawler:

    def __init__(self, host):
        self.host = host
        self.response = {"code":0, "title":host, "app":{}}
        self.status = False

    def add_site(self):
        session = Session()
        infosite = SiteModel(host=self.host, title=self.response['title'])
        infosite.app = json.dumps(self.response['app'])
        infosite.code = self.response['code']
        infosite.utime = datetime.now()
        session.add(infosite)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def whatapp(self):
        if self.status:
            self.response['header'] = self.dict_key_to_low(self.response['header'])
            if self.response['header'].has_key('x-powered-by'):
                self.response['app']['Language'] = self.response['header']['x-powered-by']

            if self.response['header'].has_key('server'):
                self.response['app']['Server'] = self.response['header']['server']

            #print type(self.response['app'])

    def dict_key_to_low(self, dict):
        return {key.lower():dict[key] for key in dict}

    def crawler(self, url):
        '''
        请求网站
        :param url:
        :return:
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Referer": "http://www.baidu.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        try:
            resp = requests.get(url=url, headers=headers, timeout=30, verify=False)
        except:
            return self.status

        self.status=True
        self.response['header'] = resp.headers
        self.response['code'] = resp.status_code

        if resp.encoding != None:
            if resp.encoding.lower() == 'gb2312' or resp.encoding.lower() == 'gbk':
                encoding = 'GB18030'
            else:
                encoding = resp.encoding
        else:
            encoding = 'utf-8'

        decoding = requests.utils.get_encodings_from_content(resp.text)

        if len(decoding) != 0:
            if decoding[0].lower() == 'gb2312' or decoding[0].lower() == 'gbk':
                decoding = 'GB18030'
            else:
                decoding = decoding[0]
        else:
            decoding = 'utf-8'
        try:
            self.response['body'] = resp.text.encode(encoding).decode(decoding).encode('UTF-8')
        except:
            self.response['body'] = resp.text.encode('UTF-8')

        title_re = re.findall('<title[\s|\S]*?>([\s|\S]*?)</title>', self.response['body'], re.IGNORECASE)
        if title_re:
            self.response['title'] = title_re[0]
            print title_re[0]
        return self.status

    def run(self):
        httpurl, httpsurl= "http://"+self.host, "https://" + self.host
        #print httpsurl
        if self.crawler(httpurl) is False:self.crawler(httpsurl)
        self.whatapp()
        self.add_site()


if __name__ == "__main__":
    a = SiteCrawler("www.baidu.com")
    a.run()



