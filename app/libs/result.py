# -*- coding=utf-8 -*-
"""
    Desc: 
    Auth: EwdAger
    Date: 2020/2/11
"""


class Result:
    result_code = 200
    success = 'true'
    result = None

    def __init__(self, result=None, result_code=None, success=None):
        if result_code:
            self.result_code = result_code
        if success:
            self.success = success
        if result:
            self.result = result

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        if self.result:
            return ['result_code', 'success', 'result']
        return ['result_code', 'success']