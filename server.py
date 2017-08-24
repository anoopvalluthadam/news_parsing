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

import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado import gen

import jwt
import ssl
import datetime
import json
import utils
from pymongo import MongoClient
from bson import json_util


def authenticate(func):
    """
    Basic authentication
    """
    def inner(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        if username == 'admin' and password == 'iamadmin':
            encoded = jwt.encode(
                    {username: password,
                     'exp': (datetime.datetime.utcnow()
                             + datetime.timedelta(seconds=1000000))},
                    'secret', algorithm='HS256'
            )

            encoded = {'error': None, 'key': encoded.decode("utf-8")}
            func(self, encoded)
        else:
            func(self, {'error': 'Invalid username/Password',
                 'key': None})
    return inner


def authentication_required(func):
    """
    Check authentication
    """
    def inner(self):

        key = self.get_argument('key')
        try:
            decoded = jwt.decode(key, 'secret')
        except jwt.ExpiredSignatureError:
            decoded = {'error': 'ExpiredSignatureError'}
            self.clear()
            self.set_status(401)
            self.finish(json.dumps(decoded))
            return
        except jwt.InvalidTokenError:
            decoded = {'error': 'InvalidTokenError'}
            self.clear()
            self.set_status(401)
            self.finish(json.dumps(decoded))
            return
        func(self, decoded)

    return inner


class MainHandler(tornado.web.RequestHandler):
    @authenticate
    def post(self, encoded):
        self.write(json.dumps(encoded))


class JsonObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def search(keywords, db):
    """
    Get the news details from the DB
    Args:
        keywords: keywords from the client
        db (MongoClient Object): DB object
    Returns:
        results: curresponding news details
    """
    keywords = keywords.split(' ')
    print('Searching...{}'.format(str(keywords)))
    results = []
    search_attr = {'tags': {'$in': keywords}}
    try:
        # Seach in the DB and generate result
        for document in db.find(search_attr):
            data = {
                'url': document['url'],
                'content': document['text'],
                'date': str(document['date'])
            }
            results.append(data)
    except Exception as error:
        print('Search Error: "{}"'.format(str(error)))

    return json_util.dumps(results)


class NewsSearch(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        # Actual Search comes here
        keywords = self.get_argument('keywords').lower()
        data = search(keywords, self.settings['db'])
        self.write(data)
        self.finish()

    def get(self):
        # Test method
        self.write('Yey! It works')
        self.finish()


configuraion = utils.read_from_configuration('config.yaml')
connect_string = utils.get_db_connect_string(configuraion)
db = MongoClient(connect_string, ssl_cert_reqs=ssl.CERT_NONE).news.posts

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/search", NewsSearch)
], db=db)

if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
