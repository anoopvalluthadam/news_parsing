
import asyncio
from newspaper import Article

import utils
from db.np_mongodb import NPMongoDB


class Crawler(object):
    def __init__(self):
        pass

    async def parse_url(self, url, mdb):
        """
        Get the content of the URL and create appropriate dicitonary
        Args:
            url (string): url
        Returns:
            data (Dictionary): parsed data from the URL
        """
        data = {}
        article = Article(url)
        article.download()
        article.parse()
        data['authors'] = article.authors
        data['date'] = article.publish_date
        data['text'] = article.text.replace('\n', '')
        article.nlp()
        # keywords used to search the data from DB
        data['tags'] = article.keywords
        # Insert the result into DB
        asyncio.ensure_future(mdb.single_insert(data))


if __name__ == '__main__':
    crawler = Crawler()
    configuraion = utils.read_from_configuration('config.yaml')
    connect_string = utils.get_db_connect_string(configuraion)
    mdb = NPMongoDB(connect_string)

    url = ('https://www.theguardian.com/australia-news/2017/aug/'
           + '22/australia-resettles-cuban-refugees-found-clinging-to-'
           + 'lighthouse-off-florida-keys')
    # policy = asyncio.get_event_loop_policy()
    # policy.set_event_loop(policy.new_event_loop())
    loop = asyncio.get_event_loop()
    # future_tasks = asyncio.ensure_future(crawler.parse_url(url, mdb))
    future_tasks = asyncio.ensure_future(mdb.in_search(['blog', 'test']))
    asyncio.gather(future_tasks)
    try:
        print('Continuous loop...')
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        future_tasks.cancel()
    except Exception as error:
        print('Loop error: {}'.format(str(error)))
    """
    exit(1)
    configuraion = utils.read_from_configuration('config.yaml')
    connect_string = utils.get_db_connect_string(configuraion)
    mdb = NPMongoDB(connect_string)

    post = {
        'author': 'Rob',
        'test': "My fourth blog post!",
        'tags': ['pop', 'third', 'helloworld'],
        'date': datetime.datetime.utcnow()
    }
    # post_id = mdb.single_insert(client, db, post)
    # print(post_id)
    # exit(1)
    for post in mdb.in_search(['pop', 'blog']):
        print('-' * 100)
        print(post)"""
