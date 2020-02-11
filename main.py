"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: main.py
@Author: Jiabao Lin
@Date: 2020/1/27
"""
from service.crawler import Crawler
from app import create_app
from app.common_exception import APIException
import sys
from flask import Flask
from app.config import setting


app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    e_type, e_value, e_traceback = sys.exc_info()
    msg = "{0}: {1}".format(e_type.__name__, e_value)
    error_msg = "未知异常: {0}".format(msg)

    return APIException(result_msg=error_msg)


if __name__ == "__main__":
    # 生产环境使用Nginx + uwsgi部署服务

    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])


