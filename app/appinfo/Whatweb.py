#!/usr/bin/env python
#coding:utf8
#__auth__ AAA师傅

import requests
import json
import re
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
rootdir = os.path.abspath(os.path.dirname(__file__))

class Whatweb:
    def __init__(self, url):
        self.url = url
        self.result_info = {
            'url' : url,
            'state' : False,
            'title' : '',
            'app' : []
        }
        # 读取指纹裤
        self._get_fingers()
        # 获取信息
        self.response = {}
        try_num = 0
        while try_num < 2 and 'title' not in self.response:
            self.response = self._request(url)
            try_num += 1
            time.sleep(5)
        # 对比指纹裤 确定app
        if len(self.response):
            self.result_info['state'] = True
            self.result_info['title'] = self.response['title'] if 'title' in self.response else ''
            self._what_app()
        else:
            self.result_info['state'] = False


    def _what_app(self):
        # 匹配的时候全部换成小写
        _response = {
            'title' : str(self.response['title']).lower(),
            'header' : str(self.response['header']).lower(),
            'body' : str(self.response['body']).lower(),
        }
        # 一次对比指纹裤
        for _ in self.fingers:
            rule = self.fingers[_]['rule']
            for i in eval(rule):
                num_i = 0
                for head in i:
                    find_num = 0
                    for str1 in i[head]:
                        if str1.lower() in str(_response[head]):
                            find_num = find_num + 1
                    if find_num == len(i[head]):
                        num_i = num_i + 1
                if num_i == len(i):
                    self.result_info['app'].append(_.encode('utf-8'))
        self.result_info['app'] = list(set(self.result_info['app']))

    def _request(self, url):
        '''
        请求网站
        :param url:
        :return:
        '''
        response = {}
        #获取网站的 headers title body 用来对比指纹
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36",
            "Accept-Language" : "zh-CN,zh;q=0.8",
            "Referer" : "http://www.baidu.com",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        try:
            resp = requests.get(url=self.url, headers=headers, timeout=30, verify=False)
        except:
            return False
        response['header'] = resp.headers
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
            response['body'] = resp.text.encode(encoding).decode(decoding).encode('UTF-8')
        except:
            response['body'] = resp.text.encode('UTF-8')
        title_re = re.findall('<title[\s|\S]*?>([\s|\S]*?)</title>', response['body'], re.IGNORECASE)
        if title_re:
            response['title'] = title_re[0]
        return response

    def _get_fingers(self):
        '''
        获取指纹
        :return:
        '''
        f = open(rootdir+os.path.sep+'app_finger')
        self.fingers = json.loads(f.read())
        f.close()

if __name__ == '__main__':
    test = Whatweb('http://drops.wooyun.org')
    print test.result_info

