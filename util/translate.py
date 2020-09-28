# coding=utf-8
import re
import random
import requests
import hashlib
import urllib.parse
import util


class TransError(Exception):
    pass


class LanguageError(Exception):
    pass


class Translate(object):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.mysql_api = util.MysqlApi(_host='127.0.0.1', _port=3306, _user='root', _passwd='buxing123', _db='wxl',
                                       _charset='utf8')
        self.logger = util.get_logger('Translate')
        self.logger.debug('app_id=%s,app_secret=%s' % (app_id, app_secret))

    def language(self, _text):
        self.logger.debug('需要判断语言的单词为：%s' % _text)
        _src = None
        fetchone = self.mysql_api.query_one('select `type` from str_language where str_key = %s;', _text)
        if fetchone is not None:
            _src = fetchone[0]
            self.logger.debug('从数据库中查询到了单词的语言')
        else:
            self.logger.debug('从数据库中没有查询到语言，开始调用接口查询')
        if _src is None:
            salt = str(random.randint(0, 999999))
            sign = hashlib.md5((self.app_id + _text + salt + self.app_secret).encode('utf8')).hexdigest()
            http_get = util.HttpGet('https://fanyi-api.baidu.com/api/trans/vip/language')
            http_get.add_param('q', _text)
            http_get.add_param('appid', self.app_id)
            http_get.add_param('salt', salt)
            http_get.add_param('sign', sign)
            http_get.execute()
            json = http_get.get_json()
            if json['error_code'] is 0:
                self.logger.debug('查询到单词的语言，开始入库')
                _src = json['data']['src']
                if _src != 'zh':
                    _src = 'en'
                self.mysql_api.execute('insert into str_language (str_key, type) VALUE (%s,%s);', (_text, _src))
            else:
                if re.findall('\u4e00-\u9fa5', _text).__len__() > 0:
                    _src = 'zh'
                else:
                    _src = 'en'
                self.mysql_api.execute('insert into str_language (str_key, type) VALUE (%s,%s);', (_text, _src))
                return _src
        return _src

    def insert_language(self, _text, _type):
        self.mysql_api.execute('insert into str_language (str_key, type) VALUE (%s,%s);', (_text, _type))

    def trans(self, _text):
        src_ = self.language(_text)
        to_ = None
        if src_ == 'en':
            to_ = 'zh'
        elif src_ == 'zh':
            to_ = 'en'
        return self.customer_trans(_text, to_)

    def customer_trans(self, _text, _to):
        self.logger.debug('开始翻译单词，单词：%s，目标语言：%s' % (_text, _to))
        _dst = None
        fetchone = self.mysql_api.query_one('select `value` from str_trans where str_key = %s and language = %s;',
                                            (_text, _to))
        if fetchone is not None:
            self.logger.debug('数据库中查询到了结果，直接返回')
            _dst = fetchone[0]
        else:
            self.logger.debug('数据库中没有查询到结果，开始调接口查询')
        if _dst is None:
            salt = str(random.randint(0, 999999))
            sign = hashlib.md5((self.app_id + _text + salt + self.app_secret).encode('utf8')).hexdigest()
            _src = self.language(_text)
            self.logger.debug('来源语言为：%s' % _src)

            http_get = util.HttpGet('https://fanyi-api.baidu.com/api/trans/vip/translate')
            http_get.add_param('q', _text)
            http_get.add_param('appid', self.app_id)
            http_get.add_param('salt', salt)
            http_get.add_param('sign', sign)
            http_get.add_param('from', _src)
            http_get.add_param('to', _to)
            http_get.execute()
            json = http_get.get_json()
            if 'error_msg' not in json:
                self.logger.debug('翻译单词成功，开始入库')
                _dst = json['trans_result'][0]['dst']
                self.mysql_api.execute('insert into str_trans (str_key, language, value) VALUE (%s,%s,%s);',
                                       (_text, _to, _dst))
            else:
                raise TransError(json['error_msg'])
        return _dst

    def close(self):
        self.mysql_api.close()


def get_default_translate():
    return Translate('20180920000210032', 'MzP5pEEZV_QorZcHS2JF')


if __name__ == '__main__':
    translate = get_default_translate()
    print(translate.language('始终'))
    print(translate.trans('始终'))
