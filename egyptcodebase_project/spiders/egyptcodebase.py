# -*- coding: utf-8 -*-
import scrapy
from egyptcodebase_project.items import EgyptcodebaseProjectItem


class EgyptcodebaseSpider(scrapy.Spider):
    name = 'egyptcodebase'
    allowed_domains = ['www.egyptcodebase.com']
    start_urls = [
            'https://www.egyptcodebase.com/en/p/all',
            'https://www.egyptcodebase.com/ar/p/all'
        ]

    def parse(self, response):
        for url in response.css('table.province-tbl > tbody > tr > td > a'):
            prov_url = url.css('::attr(href)').extract_first()
            prov_url = response.url.replace('p/all', prov_url)
            province = url.css('::text').extract_first()
            request = scrapy.Request(url=prov_url, callback=self.parse_details)
            request.meta['province'] = province
            yield request

    def parse_details(self, response):
        province = response.meta['province']
        for row in response.css('table.province-tbl > tbody > tr'):

            item = EgyptcodebaseProjectItem()
            tds = row.css('td')

            if province:
                item['province'] = province
            office = tds[0].css('a::text').extract_first()
            address = tds[1].css('::text').extract_first()
            postal_code = tds[2].css('::text').extract_first()
            if 'https://www.egyptcodebase.com/ar' in response.url:
                print(item)
                item['lang'] = 'ar'
            item['office'] = office
            item['address'] = address
            item['postal_code'] = postal_code
            yield item

        if 'https://www.egyptcodebase.com/ar' in response.url:
            next_page = response.xpath("//a[text()='التالى']")
        else:
            next_page = response.xpath("//a[text()='Next']")

        if next_page:
            url = 'https://www.egyptcodebase.com/' + next_page.css('::attr(href)').extract_first()
            request = response.follow(url=url, callback=self.parse_details)
            request.meta['province'] = province
            yield request
