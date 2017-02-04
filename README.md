# FakeNews command-line app and Python library

FakeNews is a Python command-line application and library for building an ensembled set of classifiers to detect
fake news articles. This is a work in progress, based on basic understandings of classification problems in relation
to NLP. A first approach will attempt to create a feature space using [n-grams](https://en.wikipedia.org/wiki/N-gram)
from extracted text, select a feature subset via [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf), and build a
classifier using [random forest](https://en.wikipedia.org/wiki/Random_forest).

## Installing fakenews

* Install apt packages: sudo apt-get install python3-dev openjdk-7-jre libxml2-dev libxslt1-dev
* Install python-boilerpipe: https://github.com/misja/python-boilerpipe
* Create virtualenv: virtualenv --python=python3.4 .venv
* Activate virtualenv: . .venv/bin/activate
* Install pip requirements: pip install -r requirements.txt

## Misc Research

### Detecting fake news

The following is a list of research papers on fake news detection:
* [Automatic Deception Detection: Methods for Finding Fake News](http://onlinelibrary.wiley.com/doi/10.1002/pra2.2015.145052010082/pdf)

### Web scraping

* [Scrapy](https://scrapy.org/)
* [5 Tasty Python Web Scraping Libraries](https://elitedatascience.com/python-web-scraping-libraries)

### Text extraction

The following is a list of text extraction library evaluations:
* [Evaluation of text-extraction libraries](https://www.diffbot.com/benefits/comparison/)
