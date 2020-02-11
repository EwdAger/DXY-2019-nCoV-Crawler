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

    res = []

    if latest == '1':
        result = select_overall_new()[0]
        data = dict()
        data['countRemark'] = result[1]
        data['virus'] = result[2]
        data['infectSource'] = result[3]
        data['passWay'] = result[4]
        data['remark1'] = result[5]
        data['remark2'] = result[6]
        data['remark3'] = result[7]
        data['remark4'] = result[8]
        data['remark5'] = result[9]
        data['confirmedCount'] = result[10]
        data['suspectedCount'] = result[11]
        data['curedCount'] = result[12]
        data['deadCount'] = result[13]
        data['updateTime'] = result[14]

        res.append(data)
    else:
        result = select_overall_all()
        for i in result:
            data = dict()
            data['countRemark'] = i[1]
            data['virus'] = i[2]
            data['infectSource'] = i[3]
            data['passWay'] = i[4]
            data['remark1'] = i[5]
            data['remark2'] = i[6]
            data['remark3'] = i[7]
            data['remark4'] = i[8]
            data['remark5'] = i[9]
            data['confirmedCount'] = i[10]
            data['suspectedCount'] = i[11]
            data['curedCount'] = i[12]
            data['deadCount'] = i[13]
            data['updateTime'] = i[14]
            res.append(data)

    return jsonify(Result(res))


@api.route('/area', methods=['GET'])
def area():
    latest = '1'
    province = ''
    if 'latest' in request.args:
        latest = str(request.args['latest'])
    if 'province' in request.args:
        province = str(request.args['province'])

    res = []
    result = select_area(latest, province)
    for i in result:
        data = {
            "continents": i[11],
            "country": i[1],
            "provinceName": i[2],
            "provinceShortName": i[3],
            "confirmedCount": i[4],
            "suspectedCount": i[5],
            "curedCount": i[6],
            "deadCount": i[7],
            "comment": i[8],
            "cities": json.loads(i[9]),
            "updateTime": i[10]
        }
        res.append(data)

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

    res = []
    result = select_location(province, city, district, address)
    for i in result:
        data = {
            'province': i[1],
            'city': i[2],
            'district': i[3],
            'address': i[4],
            'longitude': i[5],
            'latitude': i[6],
            'count': i[7]
        }
        res.append(data)

    return jsonify(Result(res))


@api.route('/daily', methods=['GET'])
def daily():
    date = ''
    if 'date' in request.args:
        date = str(request.args['date'])

    res = []
    result = select_daily(date)
    for i in result:
        data = {
            'confirm': i[1],
            'suspect': i[2],
            'dead': i[3],
            'heal': i[4],
            'deadRate': i[5],
            'healRate': i[6],
            'date': i[7]
        }
        res.append(data)

    return jsonify(Result(res))
