import os
import sys
import inspect
import pytest
import asyncio
import http.client as httplib
import urllib
import json

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils # noqa


@pytest.mark.incremental
class TestNewsParsingSytemTest(object):
    @pytest.mark.asyncio
    async def test_system_basic_functionality(self, queue):
        # assume that, this URL won't be there in the DB
        IP = 'localhost'
        PORT = 8080

        test_url = (
            'https://www.theguardian.com/australia-news/2017/'
            + 'aug/24/dual-citizenship-barnaby-joyce-rival-tony-'
            + 'windsor-joins-high-court-battle-as-dates-set'
        )

        # Get Queue lenghth
        q_len = await queue.llen('mylist')
        await asyncio.sleep(q_len + 10)

        queue.lpush('mylist', test_url)

        await asyncio.sleep(60)

        params = urllib.parse.urlencode({'username': 'admin',
                                         'password': 'iamadmin'})

        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection(IP, PORT)

        conn.request("POST", "/", params, headers)
        response = conn.getresponse()
        key = json.loads(response.read().decode('utf-8'))['key']

        def get_news_details(keyword):
            params = urllib.parse.urlencode({'key': key, 'keywords': keyword})
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            conn = httplib.HTTPConnection(IP, PORT)
            conn.request("POST", "/search", params, headers)
            response = conn.getresponse()
            return response.read().decode('utf-8')
        search_result = json.loads(get_news_details('citizenship'))
        result = [result['url'] for result in search_result
                  if result['url'] == test_url]
        assert result
