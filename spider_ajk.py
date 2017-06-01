#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import os
import re
import common

class spider_ajk:
    
    #获取楼盘标题
    def getTitle(self, row):
        #获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('div', class_ = 'lp-name').find('h3').find('a').get_text()
    
    #获取楼盘地理位置
    def getAddr(self, row):
        #获取节点下html标签中div属性class=address的元素html内容
        return row.find('p', class_ = 'address').find('a').get_text()
    
    #获取楼盘价格
    def getPrice(self, row):
        #获取节点下html标签中div属性class=nhouse_price的元素html内容
        return row.findNext('div', class_ = 'favor-pos').find('p').get_text()
    
    #获取房屋类型
    def getType(self, row):
        #获取房屋类型（1居／2居／3居....大小xxx-xx）
        types = ''
        type_div = row.find_all(href=re.compile('#housetype-divid'))
        if type_div is not None :
            for tmp in type_div:
                types += tmp.get_text() + '/'
        return types
    
    #获取房源状态
    def getStatus(self, row):
        #获取房屋状态，待售、售罄、开盘
        return row.find('div', class_ = 'lp-name').find('i').get_text()
    
    #获取楼盘链接
    def getUrl(self, row):
        #获取节点下html标签中div属性class=nlcd_name的元素html内容
        return row.find('div', class_ = 'lp-name').find('h3').find('a').get('href')
     
    def main(self, field, city, max_pg):
        url = 'http://' + city + '.fang.anjuke.com/loupan/all/p' 
        cname = os.path.basename(__file__).split('.')[0]
        cookie = ''
        sc = common.spider_common(url, cookie, field, max_pg, city)
        sc.analysis(cname, 'ajk', 'infos', 'utf-8')
    
#主函数入口 
if __name__ == '__main__': 
    city = 'bj'
    max_pg = 34
    
    field = [
        ["title", u"标题"], 
        ["price", u"价格"], 
        ["type", u"类型"], 
        ["status", u"状态"], 
        ["addr", u"地理位置"],
        ["url", u"详情地址"]
    ] 
    
    spider_ajk().main(field, city, max_pg)
