# -*- coding=utf-8 -*-
"""
    Desc: 
    Auth: EwdAger
    Date: 2020/2/11
"""
import pymysql
from app.config.setting import MYSQL_SETTING

db = pymysql.connect(MYSQL_SETTING['url'], MYSQL_SETTING['user'], MYSQL_SETTING['password'],
                     MYSQL_SETTING['db'], charset=MYSQL_SETTING['charset'])


def select_overall_new():
    sql = """
        SELECT DISTINCT * FROM `overall`
        ORDER BY updateTime desc
        LIMIT 1;
    """
    db.ping(reconnect=True)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res

def select_overall_all():
    sql = """
        SELECT DISTINCT * FROM `overall`
        ORDER BY updateTime desc
    """
    db.ping(reconnect=True)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
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
            ORDER BY country="中国" DESC, confirmedCount+0 DESC, updateTime DESC
        """.format(province)
    elif latest == '0':
        sql = """
            SELECT * FROM (
            SELECT * FROM `area`
            ORDER BY updateTime DESC
            ) AS t
            WHERE provinceName LIKE '%{}%'
            ORDER BY country="中国" DESC, confirmedCount+0 DESC, updateTime DESC;
        """.format(province)

    db.ping(reconnect=True)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
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
    db.ping(reconnect=True)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res

def select_daily(date):
    sql = """
        SELECT * FROM `daily`
    WHERE Tdate LIKE '%{}%'
    """.format(date)
    db.ping(reconnect=True)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res