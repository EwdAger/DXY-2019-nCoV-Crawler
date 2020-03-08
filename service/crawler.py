"""
@ProjectName: DXY-2019-nCov-Crawler
@FileName: crawler.py
@Author: Jiabao Lin
@Date: 2020/1/21
"""
from bs4 import BeautifulSoup
from service.db import DB
from service.countryTypeMap import country_type
import re
import json
import time
import logging
import datetime
import requests
from fake_useragent import UserAgent


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
ua = UserAgent()


class Crawler:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({"user-agent": ua.random})
        self.db = DB()
        self.crawl_timestamp = int()

    def run(self):
        while True:
            self.tencent_crawler()
            self.dxy_crawler()
            # self.location_crawler()
            logger.info('所有数据爬取完毕，开始沉睡1小时')
            time.sleep(3600)
            logger.info('沉睡结束')

    def history_data_crawler(self):
        while True:
            try:
                overall = self.session.get(url="https://lab.isaaclin.cn/nCoV/api/overall?latest=0")
                area = self.session.get(url="https://lab.isaaclin.cn/nCoV/api/area")

            except requests.exceptions.ChunkedEncodingError:
                self.session.headers.update({"user-agent": ua.random})
                continue

            history_overall = json.loads(overall.text)['results']
            history_area = json.loads(area.text)['results']
            for i in history_overall:
                self.overall_parser(overall_information=i, keep_cursor=True)

            for i in history_area:
                self.history_area_parser(area=i, keep_cursor=True)

            break

    def dxy_crawler(self):
        # 全国疫情
        while True:
            logger.info('开始爬取丁香园数据')
            self.crawl_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
            try:
                r = self.session.get(url='https://3g.dxy.cn/newh5/view/pneumonia')
            except requests.exceptions.ChunkedEncodingError:
                self.session.headers.update({"user-agent": ua.random})
                continue
            soup = BeautifulSoup(r.content, 'lxml')

            overall_information = re.search(r'(\{"id".*\}\})\}',
                                            str(soup.find('script', attrs={'id': 'getStatisticsService'})))
            area_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))
            abroad_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getListByCountryTypeService2'})))

            if not overall_information or not area_information:
                continue
            logger.info('丁香园数据数据读取成功，正在写入数据库')
            self.overall_parser(overall_information=json.loads(overall_information.group(1)))
            logger.info('丁香园overall数据写入完毕')
            self.area_parser(area_information=json.loads(area_information.group(0)))
            self.abroad_parser(abroad_information=json.loads(abroad_information.group(0)))
            logger.info('丁香园area数据写入完毕')
            logger.info('丁香园数据爬取完毕')
            break

    def location_crawler(self):

        # 具体疫情区域
        while True:
            logger.info('开始爬取详细地理位置数据')
            locations = []
            try:
                fail_count, count = 0, 0
                while fail_count < 5:
                    location = self.session.get(url="https://assets.cbndata.org/2019-nCoV/{}/data.json".format(count))
                    if location.ok is True:
                        count += 1
                        locations.append(location)
                    else:
                        fail_count += 1

            except requests.exceptions.ChunkedEncodingError:
                logger.info('详细地理位置数据读取失败，正在重试')
                self.session.headers.update({"user-agent": ua.random})
                continue
            logger.info('详细地理位置数据数据读取成功，正在写入数据库')
            for location in locations:
                location = json.loads(location.text)['data']
                for i in location:
                    self.location_parser(i, keep_cursor=True)
                self.db.close_cursor()
            logger.info('详细地理位置数据爬取完毕')
            break

    def tencent_crawler(self):

        # 每日新增
        while True:
            logger.info('开始爬取腾讯数据')
            try:
                daily = self.session.get(url="https://view.inews.qq.com/g2/getOnsInfo?name=disease_other")
            except requests.exceptions.ChunkedEncodingError:
                self.session.headers.update({"user-agent": ua.random})
                logger.info('腾讯数据数据读取失败，正在重试')
                continue
            logger.info('腾讯数据数据读取成功，正在写入数据库')
            daily_json = json.loads(daily.text)['data']
            daily_dict = json.loads(daily_json)
            day_add_list = daily_dict['chinaDayAddList']
            day_list = daily_dict['chinaDayList']
            for daily in day_add_list:
                self.day_add_list_parser(daily, keep_cursor=True)
            for daily in day_list:
                self.day_list_parser(daily, keep_cursor=True)
            self.db.close_cursor()
            logger.info('腾讯数据爬取完毕')
            break

    def overall_parser(self, overall_information, keep_cursor=False):
        self.db.open_cursor()
        overall_information['countRemark'] = overall_information['countRemark'].replace(' 疑似', '，疑似').replace(' 治愈', '，治愈').replace(' 死亡', '，死亡').replace(' ', '')
        data = dict()
        data['countRemark'] = overall_information['countRemark']
        data['virus'] = self.change_remark('virus', overall_information)
        data['infectSource'] = self.change_remark('infectSource', overall_information)
        data['passWay'] = self.change_remark('passWay', overall_information)
        data['remark1'] = overall_information['remark1']
        data['remark2'] = overall_information['remark2']
        data['remark3'] = overall_information['remark3']
        data['remark4'] = overall_information['remark4']
        data['remark5'] = overall_information['remark5']
        data['confirmedCount'] = overall_information['confirmedCount']
        data['suspectedCount'] = overall_information['suspectedCount']
        data['curedCount'] = overall_information['curedCount']
        data['deadCount'] = overall_information['deadCount']
        if 'updateTime' in overall_information:
            data['updateTime'] = overall_information['updateTime']
        else:
            data['updateTime'] = self.crawl_timestamp

        is_repeat = self.db.is_repeat(collection='DXYOverall', data=data)
        if not is_repeat:
            self.db.insert(collection='DXYOverall', data=data)
        self.db.close_cursor(keep_cursor)

    @staticmethod
    def change_remark(key, data):
        res = data[key]
        if '说明' in data[key]:
            operated = 'note{}'.format(data[key][-1])
            if operated in data:
                res = data[operated]

        return res

    def province_parser(self, province_information):
        provinces = json.loads(province_information.group(0))
        for province in provinces:
            province.pop('id')
            province.pop('tags')
            province.pop('sort')
            province['comment'] = province['comment'].replace(' ', '')
            if self.db.find_one(collection='DXYProvince', data=province):
                continue
            province['crawlTime'] = self.crawl_timestamp
            province['country'] = country_type.get(province['countryType'])

            self.db.insert(collection='DXYProvince', data=province)

    def area_parser(self, area_information, keep_cursor=False):
        self.db.open_cursor()
        for area in area_information:
            area['comment'] = area['comment'].replace(' ', '')
            area['country'] = '中国'
            area['continents'] = '亚洲'
            if 'updateTime' not in area:
                area['updateTime'] = self.crawl_timestamp
            area.pop('locationId')
            area['cities'] = json.dumps(area['cities'])
            is_repeat = self.db.is_repeat(collection='DXYArea', data=area)
            if not is_repeat:
                self.db.insert(collection='DXYArea', data=area)
        self.db.close_cursor(keep_cursor)

    def abroad_parser(self, abroad_information, keep_cursor=False):
        countries = abroad_information
        self.db.open_cursor()
        for country in countries:
            country['country'] = country.get('provinceName')
            country['provinceShortName'] = country.get('provinceName')
            country['comment'] = country['comment'].replace(' ', '')

            data = dict()
            data['continents'] = country['continents']
            data['country'] = country['country']
            data['provinceName'] = country['provinceName']
            data['provinceShortName'] = country['provinceShortName']
            data['confirmedCount'] = country['confirmedCount']
            data['suspectedCount'] = country['suspectedCount']
            data['curedCount'] = country['curedCount']
            data['deadCount'] = country['deadCount']
            if 'cities' in country:
                data['cities'] = country['cities']
            else:
                data['cities'] = '[]'
            data['comment'] = country['comment']
            if 'updateTime' not in data:
                data['updateTime'] = self.crawl_timestamp

            is_repeat = self.db.is_repeat(collection='DXYArea', data=data)
            if not is_repeat:
                self.db.insert(collection='DXYArea', data=data)
        self.db.close_cursor(keep_cursor)

    def history_area_parser(self, area, keep_cursor=False):
        self.db.open_cursor()
        if area['country'] == '中国':
            area['continents'] = '亚洲'
        else:
            area['continents'] = 'temp'
        if 'cities' in area:
            area['cities'] = json.dumps(area['cities'])
        else:
            area['cities'] = '[]'
        is_repeat = self.db.is_repeat(collection='DXYArea', data=area)
        if not is_repeat:
            self.db.insert(collection='DXYArea', data=area)
        self.db.close_cursor(keep_cursor)

    def location_parser(self, location, keep_cursor=False):
        self.db.open_cursor()
        if 'longitude' not in location:
            return False
        is_repeat = self.db.is_repeat(collection='location', data=location)
        if not is_repeat:
            self.db.insert(collection='location', data=location)
        else:
            try:
                self.db.update(collection='location', data=location)
            except:
                pass
        self.db.close_cursor(keep_cursor)

    def day_add_list_parser(self, daily, keep_cursor=False):
        self.db.open_cursor()
        is_repeat = self.db.is_repeat(collection='day_add_list', data=daily)
        if not is_repeat:
            self.db.insert(collection='day_add_list', data=daily)

        self.db.close_cursor(keep_cursor)

    def day_list_parser(self, day_add_list, keep_cursor=False):
        self.db.open_cursor()
        is_repeat = self.db.is_repeat(collection='day_list', data=day_add_list)
        if not is_repeat:
            self.db.insert(collection='day_list', data=day_add_list)

        self.db.close_cursor(keep_cursor)



if __name__ == '__main__':
    crawler = Crawler()
    # crawler.location_crawler()
    crawler.dxy_crawler()
