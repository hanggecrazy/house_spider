""" 安居客房源信息抓取脚本 """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import common

class spider_ajk:
    """ 安居客脚本主类"""

    @staticmethod
    def getTitle(row):
        """ 获取楼盘标题 """

        #获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('div', class_='lp-name').find('h3').find('a').get_text()

    @staticmethod
    def getAddr(row):
        """ 获取楼盘地理位置 """

        # 获取节点下html标签中div属性class=address的元素html内容
        return row.find('p', class_='address').find('a').get_text()

    @staticmethod
    def getPrice(row):
        """ 获取楼盘价格 """

        # 获取节点下html标签中div属性class=nhouse_price的元素html内容
        return row.findNext('div', class_='favor-pos').find('p').get_text()

    @staticmethod
    def getType(row):
        """  获取房屋类型 """

        # 获取房屋类型（1居／2居／3居....大小xxx-xx）
        types = ''
        type_div = row.find_all(href=re.compile('#housetype-divid'))
        if type_div is not None:
            for tmp in type_div:
                types += tmp.get_text() + '/'
        return types

    @staticmethod
    def getStatus(row):
        """ 获取房源状态 """

        # 获取房屋状态，待售、售罄、开盘
        return row.find('div', class_='lp-name').find('i').get_text()

    @staticmethod
    def getUrl(row):
        """ 获取楼盘链接 """

        # 获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('div', class_='lp-name').find('h3').find('a').get('href')

    @staticmethod
    def main(field, city, max_pg):
        """ 入口函数 """

        url = 'http://' + city + '.fang.anjuke.com/loupan/all/p'
        cname = os.path.basename(__file__).split('.')[0]
        cookie = ''
        sc = common.spider_common(url, cookie, field, max_pg, city)
        sc.analysis(cname, 'ajk', 'infos', 'utf-8')

# 主函数入口
if __name__ == '__main__':
    ajk_city = 'bj'
    m_pg = 34

    fields = [
        ["title", u"标题"],
        ["price", u"价格"],
        ["type", u"类型"],
        ["status", u"状态"],
        ["addr", u"地理位置"],
        ["url", u"详情地址"]
    ]

    spider_ajk().main(fields, ajk_city, m_pg)
