# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class NationalreportSpider(scrapy.Spider):
    name = "nationalreport"
    base_url = 'http://nationalreport.net'
    categories = ['politics', 'media', 'world', 'business', 'entertainment', 'religion', 'health', 'sports', 'crime', 'sciencetech']
    category_url_template = '%s/category/%%s/' % base_url

    def start_requests(self):
        category_urls = [self.category_url_template % category for category in self.categories]
        for url in category_urls:
            print(url)
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        story_link_regex = '%s/[a-z]+-[a-z0-9\-]+/' % self.base_url
        page_link_regex = '%s/category/[a-z]+/page/[0-9]+' % self.base_url
        print('PAGE REGEX: %s' % page_link_regex)

        story_link_extractor = LinkExtractor(canonicalize=True, unique=True, allow=story_link_regex)
        story_links = story_link_extractor.extract_links(response)
        with open('nationalreport.com.txt', 'a') as f:
            for link in story_links:
                f.write(link.url + '\n')
        
        page_link_extractor = LinkExtractor(canonicalize=True, unique=True, allow=page_link_regex)
        page_links = page_link_extractor.extract_links(response)
        for link in page_links:
            print('PAGE LINK: %s' % link)
            yield scrapy.Request(url = link.url, callback = self.parse)
        
