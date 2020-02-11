#!/bin/sh

#激活python环境
. venv/bin/activate

#启动
uwsgi --ini /data/ncov_crawler/DXY-2019-nCoV-Crawler/uwsgi.ini --enable-threads
echo "启动命令完成"
