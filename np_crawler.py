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

import asyncio
import aioredis

from newspaper import Article

import utils
from db.np_mongodb import NPMongoDB


class Crawler(object):

    async def parse_url(self, mdb):
        """
        Get the content of the URL and create appropriate dicitonary
        Args:
            url (string): url
        Returns:
            data (Dictionary): parsed data from the URL
        """
        self.redis = await aioredis.create_redis(('localhost', 6379))
        while True:
            # Data extraction from the URL
            url = await self.redis.lpop('mylist')
            if url:
                url = url.decode("utf-8")
                data = {}
                try:
                    article = Article(url)
                except Exception as error:
                    print('Article Error: {}'.format(str(error)))
                try:
                    article.download()
                except Exception as error:
                    print('Article Download Error: {}'.format(str(error)))
                    continue
                try:
                    article.parse()
                except Exception as error:
                    print('Article parse Error: {}'.format(str(error)))
                    continue
                data['authors'] = article.authors
                data['date'] = article.publish_date
                data['text'] = article.text.replace('\n', '')
                article.nlp()
                # keywords used to search the data from DB
                data['tags'] = article.keywords
                # Insert the result into DB
                data['url'] = url
                asyncio.ensure_future(mdb.single_insert(data))
            else:
                print('queue empty...')
                await asyncio.sleep(3)


if __name__ == '__main__':

    crawler = Crawler()
    # Get configuration
    configuraion = utils.read_from_configuration('config.yaml')
    connect_string = utils.get_db_connect_string(configuraion)
    mdb = NPMongoDB(connect_string)

    loop = asyncio.get_event_loop()
    future_tasks = asyncio.ensure_future(crawler.parse_url(mdb))
    asyncio.gather(future_tasks)
    try:
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
    except Exception as error:
        print('Loop error: {}'.format(str(error)))
