# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EinfomaxNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #press = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    w_date = scrapy.Field()
    pass
