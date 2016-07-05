#!/usr/bin/env python
#coding:utf-8
#author:Trip1eA

'''
从fofa.so 中获取 所有的子域名字典
'''
import requests
import re
import sys

# def _fofa_sub(target):
#     # 从fofa网站获取子域名
#     s = requests.Session()
#     req = s.get(url = 'http://fofa.so/lab/ips')
#     token = re.compile('<input type="hidden" name="authenticity_token" value="(.*?)" />').findall(req.text)[0]
#     req = s.post(url = 'http://fofa.so/lab/ips', data= {'utf8':'✓', 'authenticity_token':token, 'all':'true', 'domain':target})
#     domainlist = re.compile('<a target="_blank" href="(http://|https://)(.*?)[":]').findall(req.text)
#     resu = []
#     for subdomain in domainlist:
#         subdomain = subdomain[1]
#         if target in subdomain:
#             resu += subdomain.replace('http://','').replace('https://','').replace('.'+target, '').split('.')
#     return list(set(resu))


def _alexa_sub(target):
    # 从alexa.cn 获取子域名
    req = requests.get(url = 'http://www.alexa.cn/index.php?url=' + target)
    info = re.compile(r'showHint\(\'(.*?),(.*?),(.*?)\'\);').findall(req.text)
    payload = {'url':target, 'sig':info[0][1], 'keyt':info[0][2]}
    req = requests.post(url = 'http://www.alexa.cn/api_150710.php', data = payload)
    domainlist = re.compile('[A-Za-z0-9]*\.'+target).findall(req.text)
    resu = []
    for subdomain in domainlist:
        resu += subdomain.replace('.'+target, '').split('.')
    return list(set(resu))

def _links_sub(target):
    # 从links网站获取子域名
    req = requests.post(url = 'http://i.links.cn/subdomain/', data= {'domain':target, 'b2':'1', 'b3':'1', 'b4':'1'})
    domainlist = re.compile(r'\.<a href="(\S*?)" rel=nofollow target=_blank>(\S*?)</a></div>').findall(req.text)
    resu = []
    for subdomain in domainlist:
        resu += subdomain[0].replace('http://','').replace('https://','').replace('.'+target, '').split('.')
    return list(set(resu))

def load_net_suffix(domain):

    links_sub_dic=aleax_sub_dic=[]
    try:
    	links_sub_dic = _links_sub(domain)
    	print 'add suffix from links about %d' % len(links_sub_dic)
    except:
	    pass
    try:
    	alexa_sub_dic = _alexa_sub(domain)
    	print 'add suffix from alexa_sub_dic about %d' % len(alexa_sub_dic)
    except:
	    pass

    net_sub = list(set(links_sub_dic + alexa_sub_dic))
    f = open('../tmp.dic', 'w')
    for sub in net_sub:
        f.write(sub+'\n')
    f.close()
    print '%d all suffix write tmp done!' % len(net_sub)
    return net_sub


if __name__ == '__main__':
    load_net_suffix('baidu.com')
