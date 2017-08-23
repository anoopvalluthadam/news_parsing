
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
            url = await self.redis.lpop('mylist')
            print('-' * 100)
            print(url)
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

    configuraion = utils.read_from_configuration('config.yaml')
    connect_string = utils.get_db_connect_string(configuraion)
    mdb = NPMongoDB(connect_string)

    loop = asyncio.get_event_loop()
    future_tasks = asyncio.ensure_future(crawler.parse_url(mdb))
    asyncio.gather(future_tasks)
    try:
        print('Continuous loop...')
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
    except Exception as error:
        print('Loop error: {}'.format(str(error)))
