# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class PrntlySpider(scrapy.Spider):
    name = 'prntly'
    allowed_domains = ['prntly.com']

    def start_requests(self):
        start_urls = ['http://prntly.com/']
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        story_link_regex = 'http://prntly\.com/[0-9]{,4}/[0-9]{,2}/[0-9]{,2}/[a-z\-]+/'
        page_link_regex = 'http://prntly.com/page/[0-9]+/'

        story_link_extractor = LinkExtractor(canonicalize=True, unique=True, allow=story_link_regex)
        story_links = story_link_extractor.extract_links(response)
        with open('prntly.com.txt', 'a') as f:
            for link in story_links:
                f.write(link.url + '\n')
        
        page_link_extractor = LinkExtractor(canonicalize=True, unique=True, allow=page_link_regex)
        page_links = page_link_extractor.extract_links(response)
        for link in page_links:
            yield scrapy.Request(url = link.url, callback = self.parse)

