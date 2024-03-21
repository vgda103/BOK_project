# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class EdailyNewsPipeline:
#     def process_item(self, item, spider):
#         return item

from scrapy.exporters import CsvItemExporter, XmlItemExporter, JsonItemExporter
from scrapy.exceptions import DropItem

# Edaily Pipline
class EdailyCsvPipeline(object):
    def __init__(self):
        self.file = open("../assets/edaily_news.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
        
        self.ids_seen = set()
        
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self, item, spider):        
        self.exporter.export_item(item)
        
        if item['id'] in self.idx_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            
        return item
    