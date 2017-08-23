import asyncio
from pymongo import MongoClient
import motor.motor_asyncio


class NPMongoDB(object):
    def __init__(self, connect_string, user='admin', password='iamadmin',
                 db=None):
        """
        Constructor, Create a MongoDB connection
        Args:
            connect_string (string): Connect string for DB
        """
        self.client = None

        if not db:
            try:
                self.client = motor.motor_asyncio.AsyncIOMotorClient(
                    connect_string)
                print('DB connected...')
            except Exception as error:
                print('DB connection Error "{}"'.format(str(error)))
                exit(1)
            self.db = self.client.news
        else:
            self.db = db

    async def single_insert(self, data):
        """
        Single data insertion into DB
        Args:
            client (MongoClient): MongoDB client object
            data (Dictionary): Data to be inserted into the DB
        Returns:
            post_id (pymongo.results.InsertOneResult object): Post ID
        """
        exists = await self.db.posts.find_one({'url': data['url']})
        if not exists:
            post_id = await self.db.posts.insert_one(data)
            print('Data inserted...')
            return post_id
        print('{} exists in the DB...'.format(data['url']))

    async def in_search(self, attr, field):
        """
        Search the attr items
        Example: Post1 = {tags: [a, b, c, d]}, post2 = {a, b, c}
        attr = [a, d] will return only post 1
        Args:
            db (MongoClient DB object): Database Object
            attr (list): search items
        Returns:
            result (MongoClient search result Obj): Search result

        """
        results = []
        search_attr = {field: {'$in': attr}}
        try:
            cursor = self.db.posts.find(search_attr)
            for document in await cursor.to_list(length=100):
                results.append(document)
        except Exception as error:
            print('Search Error: "{}"'.format(str(error)))

        return results
