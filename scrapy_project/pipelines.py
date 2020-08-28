# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from env import game, mysqlInfo


class MysqlPipeline:
    user = 'root'
    password = mysqlInfo['password']
    autocommit = True

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           database=self.database,
                                           autocommit=self.autocommit)
        self.cursor = self.cnx.cursor(prepared=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        try:
            self.cursor.execute(
                self.query,
                tuple(adapter[field_name] for field_name in self.field_names))
        except mysql.connector.Error as err:
            raise DropItem(str(err))

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()


class DoubanPipeline(MysqlPipeline):
    database = 'douban'
    query = '''
    REPLACE INTO top250 (
        serial_number,
        movie_name, introduce,
        rating,
        evaluate,
        description
    )
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    field_names = ('serial_number', 'movie_name', 'introduce', 'rating',
                   'evaluate', 'description')


class GamePipeline(MysqlPipeline):
    database = game['mysql']
    query = '''
    REPLACE INTO downlink (id, download, bonus, activation)
    VALUES (?, ?, ?, ?)
    '''
    field_names = ('id', 'download', 'bonus', 'activation')
