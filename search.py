import http.client as httplib
import urllib
import json
import optparse

params = urllib.parse.urlencode({'username': 'admin', 'password': 'iamadmin'})

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost", 8888)

conn.request("POST", "/", params, headers)
response = conn.getresponse()
key = json.loads(response.read().decode('utf-8'))['key']
print(key)


def get_news_details(keyword):
    params = urllib.parse.urlencode({'key': key, 'keywords': keyword})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/search", params, headers)
    response = conn.getresponse()
    print('#' * 100)
    print(response.status, response.read())


if __name__ == '__main__':

    get_news_details('prince harry')
