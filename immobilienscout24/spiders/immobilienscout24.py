# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from realestate_crawler.items import RealestateCrawlerItem
from pandas import DataFrame

class Immobilienscout24Spider(scrapy.Spider):
    name = "immobilienscout24"
    allowed_domains = ["www.immobilienscout24.de"]
    start_urls = (
        'https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Bayern/Muenchen/','https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin/'
    )
    app_df = DataFrame()
    
    def parse(self, response):
        sel = response.xpath('//div[@class="result-list-entry__data"]')
        #sel = response.xpath('//div[@class="result-list__listing"]')
        il = ItemLoader(item=RealestateCrawlerItem(),selector=sel)

        il.add_xpath('url', 'a[@class="result-list-entry__brand-title-container"]/@href')
        il.add_xpath('title', 'a[@class="result-list-entry__brand-title-container"]/h5/text()')
        il.add_xpath('address', 'div[@class="result-list-entry__address nine-tenths"]/span/text()')
        il.add_xpath('rent', 'div[@class="result-list-entry__criteria margin-bottom-s"]/div/dl[1]/dd')
        il.add_xpath('space', 'div[@class="result-list-entry__criteria margin-bottom-s"]/div/dl[2]/dd')
        il.add_xpath('rooms', 'div[@class="result-list-entry__criteria margin-bottom-s"]/div/dl[3]/dd')

        data = il.load_item()

        try:
                df = DataFrame({'url': data['url'], 'title': data['title'], 'address' : data['address'],'rent' : data['rent'], 'space' : data['space'], 'rooms' : data['rooms']})
                self.app_df.append(df)
        except Exception,e:
                print ('Error parsing: ', response.url)
                print e
        
        next_page = response.xpath('//div[@id="pager"]/div[3]/a/@href').extract_first()

        print(next_page)
        yield scrapy.Request(response.urljoin(next_page), callback=self.parse)