from scrapy import signals
# from scrapy.exporters import CsvItemExporter
import csv


class EgyptcodebaseProjectPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('result_en_{}.csv'.format(spider.name), 'w', newline='', encoding='utf-8-sig')
        self.writer = csv.writer(self.file, delimiter=';')
        self.writer.writerow(['province', 'office', 'address', 'postal_code'])

        self.file_ar = open('result_ar_{}.csv'.format(spider.name), 'w', newline='', encoding='utf-8-sig')
        self.writer_ar = csv.writer(self.file_ar, delimiter=';')
        self.writer_ar.writerow(['province', 'office', 'address', 'postal_code'])

    def spider_closed(self, spider):
        self.file.close()
        self.file_ar.close()

    def process_item(self, item, spider):
        if 'lang' in item:
            self.writer_ar.writerow([item['province'], item['office'], item['address'], item['postal_code']])
        else:
            self.writer.writerow([item['province'], item['office'], item['address'], item['postal_code']])
        return item
