from pymongo import MongoClient


class NPMongoDB(object):
    def __init__(self, connect_string, user='admin', password='iamadmin',
                 db=None):
        """
        Constructor, Create a MongoDB connection
        Args:
            connect_string (string): Connect string for DB
        """
        client = None
        try:
            client = MongoClient(connect_string)
        except Exception as error:
            print('DB connection Error "{}"'.format(str(error)))
            exit(1)

        self.client = client

        if not db:
            self.db = client.news
        else:
            self.db = db

    def single_insert(self, data):
        """
        Single data insertion into DB
        Args:
            client (MongoClient): MongoDB client object
            data (Dictionary): Data to be inserted into the DB
        Returns:
            post_id (pymongo.results.InsertOneResult object): Post ID
        """
        post_id = self.db.insert_one(data)

        return post_id

    def in_search(self, attr):
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
        result = None
        search_attr = {'tags': {'$in': attr}}
        try:
            result = self.db.posts.find(search_attr)
        except Exception as error:
            print('Search Error: "{}"'.format(str(error)))

        return result
