# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class EmpirenewsSpider(scrapy.Spider):
    name = "empirenews"
    domain = "empirenews.net"
    allowed_domains = ['prntly.com']

    def start_requests(self):
        pages = range(1,243)
        page_url = 'http://empirenews.net/page/%s/'
        urls = [page_url % page for page in pages]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        story_link_regex = 'http://%s/[a-z\-]+/' % self.domain

        story_link_extractor = LinkExtractor(canonicalize=True, unique=True, allow=story_link_regex)
        story_links = story_link_extractor.extract_links(response)
        with open('%s.txt' % self.domain, 'a') as f:
            for link in story_links:
                f.write(link.url + '\n')
