import re
import requests

categories = ['politics', 'media', 'world', 'business', 'entertainment', 'religion', 'health', 'sports', 'crime', 'sciencetech']
category_url_template = 'http://nationalreport.net/category/%s/'
category_urls = [category_url_template % category for category in categories]

page_url_template = 'http://nationalreport.net/category/%s/page/%d/'

article_reg = re.compile('http://nationalreport\.net/[a-z]+-[a-z0-9\-]+/')
page_reg = re.compile('http://nationalreport.net/category/[a-z]+/page/[0-9]+')

with open('nationalreport.net.txt', 'a') as f:
    for category_url in category_urls:
        category_page = requests.get(category_url)
        articles
        for page_url in page_urls:
            page = requests.get(page_url)
            for match in reg.findall(str(page.content)):
                if anti_reg.search(match) == None:
                    f.write('%s\n' % match)
            f.flush()

