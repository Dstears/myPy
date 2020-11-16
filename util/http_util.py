import urllib.parse
import requests
import util


class HttpGet(object):
    def __init__(self, url):
        self.url: str = url
        self.resp = None
        self.logging = util.get_logger('HttpGet')

    def add_param(self, key, value):
        if self.url.__contains__('?'):
            self.url = self.url + '&'
        else:
            self.url = self.url + '?'
        self.url = self.url + key + '=' + urllib.parse.quote(value)
        return self

    def get_url(self):
        return self.url

    def execute(self):
        self.logging.debug('httpGet请求：%s' % self.url)
        self.resp = requests.get(self.url, timeout=5)

    def get_json(self):
        return self.resp.json()

    def get_text(self):
        return self.resp.text


if __name__ == '__main__':
    http_get = HttpGet('https://fanyi-api.baidu.com/api/trans/vip/language')
    http_get.add_param('q', 'dada')
    http_get.execute()
    print(http_get.get_json())
