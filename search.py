
import http.client as httplib
import urllib
import json
import argparse


def get_key(IP, PORT):
    params = urllib.parse.urlencode({'username': 'admin',
                                     'password': 'iamadmin'})

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection(IP, PORT)

    conn.request("POST", "/", params, headers)
    response = conn.getresponse()
    key = json.loads(response.read().decode('utf-8'))['key']
    return key


def get_news_details(keyword, IP, PORT, key):
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
    parser.add_argument("--port", help="Webserver PORT",
                        action="store", dest='PORT', type=int,
                        required=True)
    parser.add_argument("--ip", help="Webserver IP",
                        action="store", dest='IP',
                        default='localhost')
    options = parser.parse_args()
    key = get_key(options.IP, options.PORT)
    for res in json.loads(get_news_details(
            options.keywords, options.IP, options.PORT, key)):
        print(res)
