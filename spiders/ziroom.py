# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from tutorial.items import NewTutorialItem
import re
class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['ziroom.com']
    start_urls = ['http://www.ziroom.com/z/nl/z3-d23008613.html?p=1']

    def parse(self, response):

        next_url = response.xpath('//*[@id="page"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield Request('http:'+next_url,callback=self.parse)

        ziroomitem = NewTutorialItem()
        for sigdata in response.xpath('//*[@id="houseList"]/li[@class="clearfix"]'):
            ziroomitem['name'] = sigdata.xpath('div[2]/h3/a/text()').extract_first()
            ziroomitem['location'] = sigdata.xpath('div[2]/h3/a/text()').extract_first()
            ziroomitem['url'] = 'http:'+sigdata.xpath('div[2]/h3/a/@href').extract_first()
            #ziroomitem['area'] = sigdata.xpath('div[2]/div[@class="detail"]/p[1]/span[1]/text()').extract_first()
            ziroomitem['area'] = re.findall(r'[\d\.]+',sigdata.xpath('div[2]/div[@class="detail"]/p[1]/span[1]/text()').extract_first())[0]
            ziroomitem['floor'] = sigdata.xpath('div[2]/div[@class="detail"]/p[1]/span[2]/text()').extract_first()
            ziroomitem['room'] = sigdata.xpath('div[2]/div[@class="detail"]/p[1]/span[3]/text()').extract_first()
            ziroomitem['subway'] = sigdata.xpath('div[2]/div[@class="detail"]/p[2]/span/text()').extract_first()
            ziroomitem['price'] = re.findall(r'\d+',sigdata.xpath('div[3]/p[@class="price"]/text()').extract_first())[0]
            yield ziroomitem
