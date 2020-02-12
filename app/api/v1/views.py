# -*- coding=utf-8 -*-
"""
    Desc: 
    Auth: EwdAger
    Date: 2020/2/11
"""

from flask import jsonify, request
from . import api
from .utils import select_overall_new, select_overall_all, select_area, select_location, select_daily
from app.libs.result import Result
import json


@api.route('/overall', methods=['GET'])
def overall():
    latest = '1'
    if 'latest' in request.args:
        latest = str(request.args['latest'])

    if latest == '1':
        res = select_overall_new()

    else:
        res = select_overall_all()

    return jsonify(Result(res))


@api.route('/area', methods=['GET'])
def area():
    latest = '1'
    province = ''
    if 'latest' in request.args:
        latest = str(request.args['latest'])
    if 'province' in request.args:
        province = str(request.args['province'])

    res = select_area(latest, province)

    return jsonify(Result(res))


@api.route('/location', methods=['GET'])
def location():
    province, city, district, address = '', '', '', ''

    if 'province' in request.args:
        province = str(request.args['province'])
    if 'city' in request.args:
        city = str(request.args['city'])
    if 'district' in request.args:
        district = str(request.args['district'])
    if 'address' in request.args:
        address = str(request.args['address'])

    res = select_location(province, city, district, address)

    return jsonify(Result(res))


@api.route('/daily', methods=['GET'])
def daily():
    date = ''
    if 'date' in request.args:
        date = str(request.args['date'])

    res = select_daily(date)

    return jsonify(Result(res))
