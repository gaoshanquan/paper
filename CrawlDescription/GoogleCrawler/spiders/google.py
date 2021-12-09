import scrapy
from GoogleCrawler.items import GoogleItem
from GoogleCrawler.Filter import filters
import re
import pymysql
import os


def connect_sql():
    db = pymysql.connect(
        host='localhost',
        port=1108,
        user='root',
        passwd='root',
        db='googleplaystore',
        charset='utf8mb4'
    )
    return db


def getUrlFromDb():
    database = connect_sql()
    cursor = database.cursor()
    sql = "select id from photograph"
    cursor.execute(sql)
    results = cursor.fetchall()
    urls = []
    for result in results:
        app_id = result[0]
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=en'
        urls.append(url)
    database.close()
    return urls


def getData():
    app_ids = os.listdir("E:/Python project/UiReview/ui/ui_folder")
    urls = []
    for id in app_ids:
        url = 'https://play.google.com/store/apps/details?id='+id + '&hl=en'
        urls.append(url)
    return urls


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['play.google.com']

    # start_urls = ['https://play.google.com/store/apps/details?id=video.player.videoplayer&hl=en']

    start_urls = getData()
    def parse(self, response):
        item = GoogleItem()
        rule = "https://play.google.com/store/apps/details\?id=(.*)&hl=en"
        # id
        r = re.findall(rule, response.url)
        item['appID'] = r[0]
        # 类别
        category = response.xpath("//a[@class='hrTbp R8zArc']/text()").extract()
        item['category'] = category[1]
        # 描述文本
        description = response.xpath("//div[@jsname='sngebd']").extract()
        text = description[0]
        description = filters(text)
        description = description.replace("'", "''")
        item['description'] = description
        # 更新文本
        texts = response.xpath("//div[@jsname='bN97Pc']").extract()
        text = texts[1]
        text = filters(text)
        release_text = text.replace("'", "''")
        item['releaseText'] = release_text
        # print (item['releaseText'])
        yield item

