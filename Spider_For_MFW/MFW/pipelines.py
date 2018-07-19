# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import MFW.spiders.MyEncode
import sys
import io
from scrapy.conf import settings
import pymysql

class MfwPipeline(object):
    def __init__(self):
        self.f = open(r"result\xian.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False, cls=MFW.spiders.MyEncode.MyEncoder) + "\n\n\n"
        self.f.write(data)
        # host = settings['MYSQL_HOSTS']
        # user = settings['MYSQL_USER']
        # psd = settings['MYSQL_PASSWORD']
        # db = settings['MYSQL_DB']
        # c = settings['CHARSET']
        # port = settings['MYSQL_PORT']
        # # 数据库连接
        # con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # # 数据库游标
        # cue = con.cursor()
        # print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        # # sql="insert into gamerank (rank,g_name,g_type,g_status,g_hot) values(%s,%s,%s,%s,%s)" % (item['rank'],item['game'],item['type'],item['status'],item['hot'])
        # try:
        #     cue.execute("insert into TN (destination, title, time, author, content) values(%s,%s,%s,%s,%s)",
        #                 [item['destination'], item['title'], item['time'], item['author'], item['content']])
        #     print("insert success")  # 测试语句
        # except Exception as e:
        #     print('Insert error:', e)
        #     con.rollback()
        # else:
        #     con.commit()
        # con.close()

        return item

    def close_spider(self, spider):
        self.f.close()
