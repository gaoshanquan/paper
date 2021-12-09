# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

import openpyxl


def connect_sql_google():
    db = pymysql.connect(
        host='localhost',
        port=1108,
        user='root',
        passwd='root',
        db='apprecommend',
        charset='utf8mb4'
    )
    return db


def writeSQL(item):
    database = connect_sql_google()
    cursor = database.cursor()
    sql = "INSERT INTO gao_paper5(id, description, category, release_text) VALUES('%s', '%s', '%s', '%s')" % (
              item['appID'],  item['description'], item['category'], item['releaseText'])
    cursor.execute(sql)
    database.commit()
    database.close()


class GooglecrawlerPipeline:
    def process_item(self, item, spider):
        writeSQL(item)
        return item
