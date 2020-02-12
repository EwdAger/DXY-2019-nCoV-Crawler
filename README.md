# 2019新型冠状病毒疫情实时爬虫

## 请求接口：/api/v1/overall
**请求方式：GET**

返回自爬虫运行开始（2020年1月24日下午4:00）至今，病毒研究情况以及全国疫情概览，可指定返回数据为最新发布数据或时间序列数据

变量名|注释
---|---
latest	1:|返回最新数据（默认）
0：|返回时间序列数据

返回数据

变量名|	注释
---|---
countRemark|	全国疫情信息概览
virus|	病毒名称
infectSource|	传染源
passWay|	传播途径
remarkX|	注释内容，X为1~5
confirmedCount|	确诊人数
suspectedCount|	疑似感染人数
curedCount|	治愈人数
deadCount|	死亡人数
updateTime|	数据最后变动时间


## 请求接口：/api/v1/area
**请求方式：GET**
返回自2020年1月22日凌晨3:00（爬虫开始运行）至今，中国所有省份、地区或直辖市及世界其他国家的所有疫情信息变化的时间序列数据（精确到市），能够追溯确诊/疑似感染/治愈/死亡人数的时间序列。
注：自2020年1月22日凌晨3:00至2020年1月24日凌晨3:40之间的数据只有省级数据，自2020年1月24日起，丁香园才开始统计并公开市级数据。

变量名|	注释
---|---
latest	1：|返回最新数据（默认）
0：|返回时间序列数据
province	|省份、地区或直辖市，如：湖北省、香港、北京市。

返回数据

变量名|	注释
---|---
continents | 所属洲际
country|	国家名称
provinceName|	省份、地区或直辖市全称
provinceShortName|	省份、地区或直辖市简称
confirmedCount|	确诊人数
suspectedCount|	疑似感染人数
curedCount|	治愈人数
deadCount|	死亡人数
comment|	其他信息
cities|	下属城市的情况
updateTime|	数据更新时间

示例
1. /api/v1/area?latest=1&province=湖北省

    返回湖北省疫情最新数据

2. /api/v1/area?latest=0&province=湖北省

    返回湖北省疫情的时间序列数据

3. /api/v1/area?latest=1

    返回中国全部城市及世界其他国家疫情最新数据

## 请求接口：/api/v1/location
**请求方式：GET**
返回全国有记录的病患具体所在位置，各参数支持模糊搜索

变量名|注释
---|---
province| 所在省份
city| 所在城市
district | 所在直辖区
address | 详细地址

返回数据

变量名|注释
---|---
province| 所在省份
city| 所在城市
district | 所在直辖区
address | 详细地址
longitude| 经度
latitude| 纬度
count| 总计人数

# 请求接口：/api/v1/daily
**请求方式：GET**
返回每日新增确诊、疑似等数据

变量名|注释
---|---
date| 日期（例1.20，返回1月20号数据）


返回数据


变量名|注释
---|---
confirm|新增确诊
suspect|新增疑似
dead|新增死亡
heal|新增治愈
deadRate| 当前死亡比例
healRate| 当前治愈比例
date| 日期

实例：

1. /api/v1/daily

    返回从统计时间起每日新增人数

2. /api/v1/daily?date=1.20

    返回1月20日的新增数据
    
# 请求接口：/api/v1/dailyCombined
**请求方式：GET**
返回每日累计确诊、疑似等数据

变量名|注释
---|---
date| 日期（例1.20，返回1月20号数据）


返回数据


变量名|注释
---|---
confirm|累计确诊
suspect|累计疑似
dead|累计死亡
heal|累计治愈
deadRate| 当前死亡比例
healRate| 当前治愈比例
date| 日期

实例：

1. /api/v1/dailyCombined

    返回从统计时间起每日累计人数

2. /api/v1/dailyCombined?date=1.20

    返回1月20日的累计数据