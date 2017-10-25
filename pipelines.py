# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import datetime
import leveldb


dbuser = 'luna'
dbpass = 'luna'
dbname = 'ofo'
dbhost = '127.0.0.1'
dbport = '3306'
 
class TutorialPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.cursor.execute("truncate table ziroom_house;")
        self.conn.commit() 
        self.dblevel = leveldb.LevelDB('./ziroomdb')
    def process_item(self, item, spider): 
        curTime = datetime.datetime.now().strftime("%Y-%m-%d") 
        try:
            self.cursor.execute("""INSERT INTO ziroom_house (name, location, url, area, floor, room,subway,price,updatetime)  
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                            (
                                item['name'].encode('utf-8'), 
                                item['location'].encode('utf-8'),
                                item['url'].encode('utf-8'),
                                item['area'].encode('utf-8'),
                                item['floor'].encode('utf-8'),
                                item['room'].encode('utf-8'),
                                item['subway'].encode('utf-8'),
                                item['price'].encode('utf-8'),
                                curTime,
                            )
            )
     
            self.conn.commit()
     
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        self.dblevel.Put(item['url'].encode('utf-8'),item['name'].encode('utf-8')) 
        return item

