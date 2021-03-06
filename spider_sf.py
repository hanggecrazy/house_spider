""" 搜房房源信息抓取脚本 """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import common

class spider_sf:
    """ 脚本主类 """

    @staticmethod
    def getTitle(row):
        """ 获取楼盘信息 """

        # 获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('div', class_="nlcd_name").find('a').get_text()

    @staticmethod
    def getAddr(row):
        """ 获取楼盘地址位置信息 """

        # 获取节点下html标签中div属性class=address的元素下的a标签下的span标签下的html内容
        addr_div = row.find('div', class_='address').find('a')
        if addr_div.find('span') is not None:
            # 获取当前元素下的span标签的内容"""
            addr = addr_div.find('span').get_text()
            if addr_div.get('title') is not None:
                # 存在span标签将span标签内容和a标签内容组合
                addr += addr_div.get('title')
        else: # 不存在span标签将span标签内容和a标签内容组合拼接
            addr = addr_div.get_text() + addr_div.get('title')

        return addr

    @staticmethod
    def getPrice(row):
        """ 获取楼盘价格 """

        # 获取节点下html标签中div属性class=nhouse_price的元素html内容
        price_div = row.find('div', class_='nhouse_price')

        if price_div is not None:
            price = price_div.find('span').get_text()
            # 获取当前元素下的em标签
            if price_div.find('em') is not None:
                # 拼接当前元素下的em标签内容
                price += price_div.find('em').get_text()
        elif row.find('div', class_='kanzx') is not None:
            # 不存在div标签时获取div属性class=kanesf的div文本内容
            price = row.find('div', class_='kanzx').find('h3').find('a').get_text()
        else:
            price = row.find('div', class_='kanesf').get_text()

        return price

    @staticmethod
    def getType(row):
        """ 获取房源类型 """
        # 获取房屋类型（1居／2居／3居....大小xxx-xx）
        return row.find('div', class_='house_type').get_text()

    @staticmethod
    def getStatus(row):
        """ 获取房源状态信息 """
        # 获取房屋状态，待售、售罄、开盘
        return row.find('div', class_='fangyuan').find('span').get_text()

    @staticmethod
    def getUrl(row):
        """  获取房源链接 """
        # 获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('div', class_='nlcd_name').find('a').get('href')

    @staticmethod
    def main(field, city, max_pg):
        """ 函数入口 """

        url = 'http://newhouse' + ('' if city == 'bj' else '.' + city)  + '.fang.com/house/s/b9'

        cname = os.path.basename(__file__).split('.')[0]
        cookie = ''
        sc = common.spider_common(url, cookie, field, max_pg, city)
        sc.analysis(cname, 'sf', 'nlc_details', 'gbk')

# 主函数入口
if __name__ == "__main__":

    sf_city = 'cd'
    m_pg = 101

    fields = [
        ["title", u"标题"],
        ["price", u"价格"],
        ["type", u"类型"],
        ["status", u"状态"],
        ["addr", u"地理位置"],
        ["url", u"详情地址"]
    ]

    spider_sf().main(fields, sf_city, m_pg)
