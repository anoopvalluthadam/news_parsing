
import redis
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor


class NewsSpider(scrapy.Spider):
    name = 'theguardian'
    allowed_domains = ['theguardian.com']
    start_urls = ['https://www.theguardian.com/au']

    def __init__(self, r):
        self.redis = r

    def parse(self, response):
        for url in response.css('h2.fc-item__title a::attr(href)').extract():
            print(url)
            yield {'url': url}
            self.redis.lpush('mylist', url)


def run_spider():
    """
    Run Spider
    """
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        process = CrawlerProcess({
            'USER_AGENT':
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': '/tmp/result.json'
        })

        process.crawl(NewsSpider, r)
        process.start()
    except Exception as error:
        print('Error in Spiding: {}'.format(str(error)))

    return 1


def main():
    """
    Crawl through theguardian homepage, every 1 Hour
    """
    import concurrent.futures

    with concurrent.futures.ProcessPoolExecutor() as executor:
        while 1:
            executor.submit(run_spider)
            time.sleep(3600)


if __name__ == '__main__':
    main()
