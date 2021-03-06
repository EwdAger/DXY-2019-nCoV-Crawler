"""
@ProjectName: DXY-2019-nCov-Crawler
@FileName: db.py
@Author: Jiabao Lin
@Date: 2020/1/21
"""

import pymysql
from app.libs.mysqlconn import POOL


class DB:
    def __init__(self):
        self.db = None
        self.cursor = None

    def insert(self, collection, data):
        sql, params = self.get_insert_sql(collection, data)
        self.cursor.execute(sql, params)
        self.db.commit()

    def update(self, collection, data):
        sql = self.get_update_sql(collection, data)
        self.cursor.execute(sql)
        self.db.commit()

    def open_cursor(self):
        if not self.cursor and not self.db:
            self.db = POOL.connection()
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def close_cursor(self, keep_cursor=False):
        if self.cursor and keep_cursor is False:
            self.cursor.close()
            self.db.close()
            self.cursor = None
            self.db = None
            return True
        else:
            return False

    @staticmethod
    def get_insert_sql(collection, data):
        sql = ""
        params = ()
        if collection == "DXYArea":
            sql = """
                INSERT INTO area(country, provinceName, provinceShortName, confirmedCount, suspectedCount,
                curedCount, deadCount, comment, cities, updateTime, continents)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data['country'], data['provinceName'], data["provinceShortName"], data["confirmedCount"],
                data['suspectedCount'], data['curedCount'], data['deadCount'], data['comment'], data['cities'],
                data['updateTime'], data['continents']
            )

        elif collection == "DXYOverall":
            sql = """
                INSERT INTO overall(countRemark, virus, infectSource, passWay, remark1,
                remark2, remark3, remark4, remark5, confirmedCount, suspectedCount, curedCount, deadCount, updateTime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data['countRemark'], data['virus'], data['infectSource'], data['passWay'], data['remark1'],
                data['remark2'], data['remark3'], data['remark4'], data['remark5'], data['confirmedCount'],
                data['suspectedCount'], data['curedCount'], data['deadCount'], data['updateTime']
            )

        elif collection == 'location':
            sql = """
                INSERT INTO location(province, city, district, address, longitude, latitude, count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data['province'], data['city'], data['district'], data['address'], str(data['longitude']),
                str(data['latitude']), str(data['count'])
            )

        elif collection == 'day_add_list':
            sql = """
                INSERT INTO daily(confirm, suspect, dead, heal, deadRate, healRate, Tdate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            params = (
                data['confirm'], data['suspect'], data['dead'], data['heal'], data['deadRate'], data['healRate'],
                data['date']
            )

        elif collection == 'day_list':
            sql = """
                INSERT INTO dayList(confirm, suspect, dead, heal, deadRate, healRate, Tdate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            params = (
                data['confirm'], data['suspect'], data['dead'], data['heal'], data['deadRate'], data['healRate'],
                data['date']
            )

        return sql, params

    def is_repeat(self, collection, data):
        sql = ''
        if collection == "DXYOverall":
            sql = """
                SELECT confirmedCount, suspectedCount, curedCount, deadCount
                FROM overall
                WHERE confirmedCount={} and suspectedCount={} and curedCount={} and deadCount={}
            """.format(str(data['confirmedCount']),
                       str(data['suspectedCount']), str(data['curedCount']), str(data['deadCount']))
        elif collection == "DXYArea":
            sql = """
                    SELECT provinceName, confirmedCount, suspectedCount, curedCount, deadCount
                    FROM area
                    WHERE provinceName=\"{}\" and confirmedCount={} and suspectedCount={} and curedCount={} and deadCount={}
                """.format(data['provinceName'], str(data['confirmedCount']),
                           str(data['suspectedCount']), str(data['curedCount']), str(data['deadCount']))

        elif collection == 'location':
            sql = """
                    SELECT *
                    FROM location
                    WHERE province =\"{}\" and city={} and district={} and address =\"{}\" and longitude={} and latitude={}
                """.format(data['province'], data['city'], data['district'], data['address'], str(data['longitude']),
                           str(data['latitude']))

        elif collection == 'day_add_list':
            sql = """
                SELECT *
                FROM daily
                WHERE Tdate=\"{}\"
            """.format(data['date'])

        elif collection == 'day_list':
            sql = """
                    SELECT *
                    FROM dayList
                    WHERE Tdate=\"{}\"
                """.format(data['date'])

        try:
            self.cursor.execute(sql)
            is_repeat = self.cursor.fetchall()
        except:
            is_repeat = False
        if is_repeat:
            return True
        else:
            return False

    @staticmethod
    def get_update_sql(collection, data):
        sql = ''

        if collection == 'location':
            sql = """
                UPDATE location 
                SET count=\"{}\"
                WHERE address =\"{}\" and longitude={} and latitude={}
            """.format(data['count'], data['address'], str(data['longitude']), str(data['latitude']))

        return sql
