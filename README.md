```
 _____             _____     _                 
|  ___| __ ___  __|_   _|_ _(_) ___  _ __  ___ 
| |_ | '__/ _ \/ _ \| |/ _` | |/ _ \| '_ \/ __|
|  _|| | |  __/  __/| | (_| | | (_) | |_) \__ \
|_|  |_|  \___|\___||_|\__,_|_|\___/| .__/|___/
                                    |_|  
```
简介- Taiops-自由版
---
```
Tai是泰山、ops是运维安全，但是自由版并没有带安全检测的功能，感兴趣的朋友可以自己拓展下。
自由版的主要功能：收集子域名、端口信息并保存。自建项目分类，收藏IP、域名。
采用的开发语言、框架、模块等：Python2.7、Flask以及一些拓展、Celery、Redis、MySQL

```
安装环境搭建：debian-kali
---
```
安装Flask：http://docs.jinkan.org/docs/flask/installation.html
安装redis：http://redis.io/topics/quickstart
安装MySQL：http://www.cnblogs.com/xusir/p/3334217.html
安装Python 依赖包：pip install -r requirements.txt
```
目录结构
---
```
├── app_config.xml 
├── appinfo 
│   ├── app_finger 
│   ├── __init__.py
│   ├── readme
│   ├── views.py
│   └── Whatweb.py
├── auth
│   ├── form.py
│   ├── inc.py
│   ├── __init__.py
│   └── views.py
├── common
│   ├── config.py
│   ├── domain.sufix
│   ├── formatck.py
│   ├── form.py
│   ├── __init__.py
│   └── modles.py
├── core
│   └── __init__.py
├── __init__.py
├── main
│   ├── errors.py
│   ├── form.py
│   ├── inc.py
│   ├── index.py
│   ├── __init__.py
│   ├── pojmanager.py
│   ├── project.py
│   ├── qassert.py
│   └── views.py
├── server.py
├── static
├── templates
└── worker
    ├── assertimport
    │   ├── asset_crawler.py
    │   ├── data
    │   ├── dict
    │   ├── __init__.py
    │   ├── lib
    │   └── tmp.dic
    ├── celeryconfig.py
    ├── hashid
    │   ├── hashid.py
    │   └── __init__.py
    ├── __init__.py
    ├── portcrawler
    │   ├── dict
    │   ├── __init__.py
    │   └── portcrawler.py
    ├── sitecrawler
    │   ├── __init__.py
    │   └── sitecrawler.py
    ├── tasks.py
    └── tmp.dic
```
