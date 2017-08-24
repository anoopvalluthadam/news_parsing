# -*- coding: utf-8; -*-
#

# This file is part of Mandriva Management Console (MMC).
#
# News Parsing is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# News Parsing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MMC.  If not, see <http://www.gnu.org/licenses/>.
#
# @author : Anoop Valluthadam <anoopvalluthadam@gmail.com>

import redis
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor # noqa
import concurrent.futures


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
            # Push into Redis Queue for the Crawler to use
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
    # Each Spider run in a new Process
    with concurrent.futures.ProcessPoolExecutor() as executor:
        while 1:
            executor.submit(run_spider)
            time.sleep(3600)


if __name__ == '__main__':
    main()
