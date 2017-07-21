# DFB Final Crawler
This git project is for DFB Data mining competition. It contains a crawler based on [Scrapy](https://github.com/scrapy/scrapy) that collects TV series data from [Youku Index](http://index.youku.com) and [Douban](https://www.douban.com/).

##  DFB_Series_data_crawler
The crawler.  
To activate spiders, run `scrapy crawl -o OUTPUT -a list=tv.txt micro`  or `scrapy crawl -o OUTPUT -a list=tv.txt macro`
For more information, [Scrapy Docs](docs.scrapy.org)

## Virtualenv
The virtual python environment for this project. It contains all the packages that are used in crawler.