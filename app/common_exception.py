"""
    Desc:
    Auth: Robinsen
    Date: 2019/4/30 16:10
"""
from flask import json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    result_code = 500
    result_msg = '系统错误，请联系管理员'
    code = 500
    data = None

    def __init__(self, result_msg=None, result_code=None, code=None, data=None):
        if code:
            self.code = code
        if result_code:
            self.result_code = result_code
        if result_msg:
            self.result_msg = result_msg
        if data:
            self.data = data
        super(APIException, self).__init__(result_msg, None)

    def get_body(self, environ=None):
        body = dict(
            result_code=self.result_code,
            result_msg=self.result_msg
        )
        if self.data:
            body = dict(
                result_code=self.result_code,
                result_msg=self.result_msg,
                data=self.data
            )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]
