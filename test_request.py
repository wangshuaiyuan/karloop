# coding=utf-8

__author__ = 'karl'


import urllib, httplib
httpClient = None
try:
    params = urllib.urlencode({'name': 'waitalone.cn', 'age': '5'})
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    httpClient = httplib.HTTPConnection('192.168.0.118', 8421, timeout=10)
    httpClient.request('GET', '/hello', params, headers)
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
    print response.getheaders()
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()