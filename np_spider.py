
import redis
import time
import scrapy
from scrapy.crawler import CrawlerProcess


class NewsSpider(scrapy.Spider):
    name = 'theguardian'
    allowed_domains = ['theguardian.com']
    start_urls = ['https://www.theguardian.com/au']

    def __init__(self, r):
        self.redis = r

    def parse(self, response):
        for url in response.css('h2.fc-item__title a::attr(href)').extract():
            print(url)
            self.redis.lpush('mylist', url)


def main():
    """
    Crawl through theguardian homepage
    """
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    while 1:
        process = CrawlerProcess({
            'USER_AGENT':
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': '/tmp/result.json'
        })

        process.crawl(NewsSpider, r)
        time.sleep(3600)

    process.start()


if __name__ == '__main__':
    main()
