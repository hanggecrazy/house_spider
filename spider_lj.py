"""链家房源信息抓取脚本"""
#!/usr/bin/env pytho3
# -*- coding: utf-8 -*-

import os
import common

class spider_lj:
    """ 脚本主类  """

    @staticmethod
    def getTitle(row):
        """ 获取楼盘标题 """

        # 获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('h2').find('a').get_text()

    @staticmethod
    def getAddr(row):
        """ 获取楼盘地理位置信息 """

        # 获取节点下html标签中div属性class=address的元素html内容
        return row.find('div', class_='where').find('span').get_text()

    @staticmethod
    def getPrice(row):
        """ 获取楼盘价格 """

        price = ""
        # 获取节点下html标签中div属性class=nhouse_price的元素html内容
        price_div = row.find('div', class_='average')

        # 判断div是否存在内容，存在则获取div下的span标签的文本内容
        if price_div is not None:
            tmp = price_div.find('span').get_text()
            if tmp is not None:
                price = tmp
        return price

    @staticmethod
    def getType(row):
        """ 获取房源状态 """

        # 获取房屋类型（1居／2居／3居....大小xxx-xx）
        types = ''
        type_div = row.find('div', class_='type').find_all('span')
        if type_div is not None:
            for tmp in type_div:
                types += tmp.get_text() + '/'

        return types

    @staticmethod
    def getArea(row):
        """ 获取房源面积大小 """
        area = ''
        # 获取房屋大小
        area_div = row.find('div', class_='area')
        if area_div is not None:
            area = area_div.get_text().replace(' ', '')

            tmp = area_div.find('span').get_text()
            if tmp is not None:
                area += tmp

        return area

    @staticmethod
    def getUrl(row):
        """ 获取楼盘链接地址 """

        # 获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('h2').find('a').get('href')

    @staticmethod
    def main(field, city, max_pg):
        """ 主函数入口 """

        url = 'http://' + city + '.fang.lianjia.com/loupan/pg'
        cname = os.path.basename(__file__).split('.')[0]
        cookie = 'lianjia_uuid=34297c8f-9728-4e96-a708-d2e6c2a21839;'
        sc = common.spider_common(url, cookie, field, max_pg, city)
        sc.analysis(cname, 'lj', 'info-panel', 'utf-8')

# 主函数入口
if __name__ == '__main__':
    lj_city = 'bj'
    m_pg = 18

    fields = [
        ["title", u"标题"],
        ["price", u"价格"],
        ["type", u"类型"],
        ["area", u"面积"],
        ["addr", u"地理位置"],
        ["url", u"详情地址"]
    ]

    spider_lj().main(fields, lj_city, m_pg)
