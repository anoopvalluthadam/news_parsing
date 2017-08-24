
import http.client as httplib
import urllib
import json
import argparse

IP = '35.194.145.97'
# IP = 'localhost'
PORT = 8080
params = urllib.parse.urlencode({'username': 'admin', 'password': 'iamadmin'})

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", help="Search words",
                        action="store", dest='keywords',
                        required=True)
    options = parser.parse_args()
    for res in json.loads(get_news_details(options.keywords)):
        print(res)
