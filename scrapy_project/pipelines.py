# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from env import game, mysqlInfo

root_password = mysqlInfo['password']


class DoubanPipeline:
    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(user='root',
                                           password=root_password,
                                           database='douban',
                                           autocommit=True)
        self.cursor = self.cnx.cursor(prepared=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        query = '''
        REPLACE INTO top250 (serial_number, movie_name, introduce, rating, evaluate, description)
        VALUES (?, ?, ?, ?, ?, ?)
        '''

        try:
            self.cursor.execute(
                query, (adapter['serial_number'], adapter['movie_name'],
                        adapter['introduce'], adapter['rating'],
                        adapter['evaluate'], adapter['description']))
        except mysql.connector.Error as err:
            raise DropItem(str(err))

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()


class GamePipeline:
    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(user='root',
                                           password=root_password,
                                           database=game['mysql'],
                                           autocommit=True)
        self.cursor = self.cnx.cursor(prepared=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        query = '''
        REPLACE INTO downlink (id, download, bonus, activation)
        VALUES (?, ?, ?, ?)
        '''
        try:
            self.cursor.execute(query,
                                (adapter['id'], adapter['download'],
                                 adapter['bonus'], adapter['activation']))
        except mysql.connector.Error as err:
            raise DropItem(str(err))

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()
