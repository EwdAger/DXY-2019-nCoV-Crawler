# -*- coding=utf-8 -*-
"""
    Desc: 
    Auth: EwdAger
    Date: 2020/2/11
"""
from service.db import DB

db = DB()


def select_overall_new():
    sql = """
        SELECT DISTINCT * FROM `overall`
        ORDER BY updateTime desc
        LIMIT 1;
    """
    res = db.execute(sql)
    return res

def select_overall_all():
    sql = """
        SELECT DISTINCT * FROM `overall`
        ORDER BY updateTime desc
    """
    res = db.execute(sql)
    return res

def select_area(latest, province):
    if latest == '1':
        sql = """
            SELECT * FROM (
            SELECT * FROM `area`
            ORDER BY updateTime DESC
            ) AS t
            GROUP BY provinceName
            HAVING provinceName LIKE '%{}%'
            ORDER BY updateTime DESC
        """.format(province)
    elif latest == '0':
        sql = """
            SELECT * FROM (
            SELECT * FROM `area`
            ORDER BY updateTime DESC
            ) AS t
            WHERE provinceName LIKE '%{}%'
            ORDER BY updateTime DESC;
        """.format(province)
    res = db.execute(sql)
    return res

def select_location(province, city, district, address):
    sql = """
        SELECT * FROM `location` 
        WHERE
            province LIKE "%{}%" 
            AND city LIKE "%{}%" 
            AND district LIKE "%{}%"
            AND address LIKE "%{}%";
    """.format(province, city, district, address)
    res = db.execute(sql)
    return res
