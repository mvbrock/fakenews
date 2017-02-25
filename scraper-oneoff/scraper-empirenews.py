import re
import requests

page_url_template = 'http://empirenews.net/page/%d/'
page_urls = [page_url_template % page_num for page_num in range(1,243)]
reg = re.compile('http://empirenews\.net/[a-z]+-[a-z0-9\-]+/')
anti_reg = re.compile('http://empirenews\.net/wp-')

with open('empirenews.net.txt', 'a') as f:
    for page_url in page_urls:
        print('getting page: %s' % page_url)
        page = requests.get(page_url)
        for match in reg.findall(str(page.content)):
            if anti_reg.search(match) == None:
                f.write('%s\n' % match)
        f.flush()

