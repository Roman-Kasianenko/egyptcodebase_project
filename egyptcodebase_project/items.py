import scrapy


class EgyptcodebaseProjectItem(scrapy.Item):
    province = scrapy.Field()
    office = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    lang = scrapy.Field()
