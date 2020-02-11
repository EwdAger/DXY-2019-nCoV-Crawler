# """
#     Desc:
#     Auth: Robinsen
#     Date: 2019/4/30 10:24
# """
from flask import Blueprint
from app.api.v1 import api


def create_blueprint_v1():
    bp_v1 = Blueprint("", __name__)
    api.register(bp_v1)
    return bp_v1
