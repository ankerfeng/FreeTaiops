```
 _____             _____     _                 
|  ___| __ ___  __|_   _|_ _(_) ___  _ __  ___ 
| |_ | '__/ _ \/ _ \| |/ _` | |/ _ \| '_ \/ __|
|  _|| | |  __/  __/| | (_| | | (_) | |_) \__ \
|_|  |_|  \___|\___||_|\__,_|_|\___/| .__/|___/
                                    |_|  
```
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) 
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
数据库结构：taiops.sql
```
目录结构
---
```
├── app_config.xml 
├── appinfo 
│   ├── app_finger 
    |...
├── auth
│   ├── form.py
│   |...
├── common
│   ├── config.py
│   |...
├── core
│   └── __init__.py
├── __init__.py
├── main
│   ├── errors.py
│   |...
├── server.py
├── static
├── templates
└── worker
    ├── assertimport
    │   ├── asset_crawler.py
    │   |...
```
配置文件
---
```
配置文件（一)
├── common
│   ├── config.py

配置文件（二)
├── common
│   └── modles.py

配置文件（三)
└── worker
    ├── celeryconfig.py
```
启动
---
```
启动celery:celery -A tasks worker --loglevel=info
启动server: (线上环境 默认)python server.py production (调试模式）python server.py development
```
![](http://dev.bugsrc.com/wp-content/uploads/2016/07/1111.png)
