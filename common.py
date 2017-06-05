""" 公共组件 """
# !/usr/bin/env python3
#  -*- coding: utf-8 -*-

import time
import urllib.request
import zlib
import xlwt

from bs4 import BeautifulSoup

class spider_common:
    """ 主类 """

    def __init__(self, url, cookie, field, max_pg, city):

        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
        ua += '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie' : cookie,
            'Proxy-Connection': 'keep-alive',
            'User-Agent': ua
        }
        self.url = url
        self.city = city
        self.field = field
        self.max_pg = max_pg

    def getData(self):
        """ 通过URL获取内容信息 """

        print(self.url)
        req = urllib.request.Request(self.url, headers=self.headers)
        data = urllib.request.urlopen(req).read()

        # 原网页html内容因为是压缩过，因此需要解压缩处理
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)

    @staticmethod
    def paraser(html, iencode, oencode='utf-8'):
        """ 解析html """

        if iencode == 'gbk' or iencode == 'gb2312' or iencode == 'gb18030':
            html = html.decode('gbk').encode(oencode)
        doc = BeautifulSoup(html, 'html.parser')

        return doc

    @staticmethod
    def trimChar(value):
        """ 去掉多余的符号 """

        if value != []:
            # 去掉网页标签中多余的换行和制表符
            return value.replace("\n", '').replace("\t", '').replace("\r\n", '')
        return value

    def getFiled(self, cname, row, field):
        """ 获取指定字段 """

        exec("import " + cname)
        value = {}

        strline = ''
        for data in field:
            name = eval(cname +'.'+ cname +'()'  + ".get" + data[0].capitalize())(row)
            value[data[0]] = self.trimChar(name)
            strline += value[data[0]] + "\t"
        print(strline)

        return value

    def analysis(self, cname, source, content_div, iencoding):
        """ 解析内容 """
        line = 0
        excel = xlwt.Workbook() # 创建excel对象

        sheet = excel.add_sheet(self.city + u"新房") # 在excel中添加新房的sheet

        for colum in range(0, len(self.field)):

            sheet.write(line, colum, self.field[colum][1]) # 在sheet中添加第line行第colum列内容

        # 循环获取1-max_pg页的房产信息
        for pg in range(1, self.max_pg):
            self.url = self.url + str(pg) + '/'
            html = self.getData() # 获取每页房产信息的html内容
            doc = self.paraser(html, iencoding, 'utf-8') # 将html内容转换为dom树节点内容

            detail_div = doc.find_all("div", class_=content_div)

            if detail_div is None:
                continue

            for row in detail_div: # 循环div属性class=nlc_details的节点内容
                line += 1 # excel行号增加
                value = self.getFiled(cname, row, self.field) # 获取需要的网页内容
                if value is None:
                    continue

                for colum in range(0, len(self.field)):
                    sheet.write(line, colum, value[self.field[colum][0]])

            time.sleep(5) # 暂停5s

        excel.save('./excel/' + self.city + '_' + source + '_house.xls')  # 保存excel
