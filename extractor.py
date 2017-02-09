from boilerpipe.extract import Extractor
import argparse
import re

parser = argparse.ArgumentParser(description = 'Text content extractor')
parser.add_argument('--urls', type=str, required=True,
    help='A new-line separated list of URLS to extract content from')
parser.add_argument('--outputdirhtml', type=str, required=True,
    help='The text output dir to store the content from each URL')
parser.add_argument('--outputdirtxt', type=str, required=True,
    help='The HTML output dir to store the content from each URL')
args = parser.parse_args()

with open(args.urls, 'r') as url_file:
    for url in url_file:
        url = url.strip()
        url_base_filename = re.sub('[^a-zA-Z0-9_\.\-]', '_', url)
        url_txt_filename = url_base_filename + ".txt"
        url_html_filename = url_base_filename + ".html"
        extractor = Extractor(extractor='ArticleExtractor', url=url)
        url_txt_contents = extractor.getText()
        url_html_contents = extractor.getHTML()
        with open(args.outputdirtxt + '/' + url_txt_filename, 'w') as txt_content_file:
            txt_content_file.write(url_txt_contents)
        with open(args.outputdirhtml + '/' + url_html_filename, 'w') as html_content_file:
            html_content_file.write(url_html_contents)

