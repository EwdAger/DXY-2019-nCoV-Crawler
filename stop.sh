#!/bin/sh

. venv/bin/activate

#停止命令
uwsgi --stop uwsgi/uwsgi.pid

sleep 5

ps -ef | grep uwsgi | grep 'multi-analysis' | awk '{print $2}' | xargs kill -9

echo "停止命令完成"
