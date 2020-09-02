# coding=utf-8
import random
import requests
import hashlib
import urllib.parse
import utils


class TransError(Exception):
    pass


class LanguageError(Exception):
    pass


class Translate(object):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.conn = utils.get_conn()
        self.logger = utils.get_logger('Translate')

        self.logger.debug('app_id=%s,app_secret=%s' % (app_id, app_secret))

    def language(self, _text):
        conn = utils.get_conn()
        cursor = conn.cursor()
        cursor.execute('select `type` from str_language where str_key = %s;', _text)
        _src = None
        fetchone = cursor.fetchone()
        if fetchone is not None:
            _src = fetchone[0]
        if _src is None:
            salt = str(random.randint(0, 999999))
            sign = hashlib.md5((self.app_id + _text + salt + self.app_secret).encode('utf8')).hexdigest()
            url = 'https://fanyi-api.baidu.com/api/trans/vip/language?q=' + urllib.parse.quote(
                _text) + '&appid=' + urllib.parse.quote(self.app_id) + '&salt=' + urllib.parse.quote(
                salt) + '&sign=' + urllib.parse.quote(sign)
            resp = requests.get(
                url)
            json = resp.json()
            if json['error_code'] is 0:
                _src = json['data']['src']
                cursor.execute('insert into str_language (str_key, type) VALUE (%s,%s);', (_text, _src))
                conn.commit()
            else:
                raise LanguageError(json['error_msg'])
        return _src

    def insert_language(self, _text, _type):
        cursor = self.conn.cursor()
        sql = cursor.mogrify('insert into str_language (str_key, type) VALUE (%s,%s);', (_text, _type))
        cursor.execute(sql)
        self.conn.commit()

    def trans(self, _text):
        src_ = self.language(_text)
        to_ = None
        if src_ == 'en':
            to_ = 'zh'
        elif src_ == 'zh':
            to_ = 'en'
        return self.customer_trans(_text, to_)

    def customer_trans(self, _text, _to):
        conn = utils.get_conn()
        cursor = conn.cursor()
        cursor.execute('select `value` from str_trans where str_key = %s and language = %s;', (_text, _to))
        _dst = None
        fetchone = cursor.fetchone()
        if fetchone is not None:
            _dst = fetchone[0]
        if _dst is None:
            salt = str(random.randint(0, 999999))
            sign = hashlib.md5((self.app_id + _text + salt + self.app_secret).encode('utf8')).hexdigest()
            _src = None

            if _src is None:
                _src = self.language(_text)
            url = 'https://fanyi-api.baidu.com/api/trans/vip/translate?q=' + urllib.parse.quote(
                _text) + '&appid=' + urllib.parse.quote(self.app_id) + '&salt=' + urllib.parse.quote(
                salt) + '&sign=' + urllib.parse.quote(sign) + '&from=' + urllib.parse.quote(
                _src) + '&to=' + urllib.parse.quote(_to)
            resp = requests.get(
                url)
            json = resp.json()
            if 'error_msg' not in json:
                _dst = json['trans_result'][0]['dst']
                cursor.execute(
                    'insert into str_trans (str_key, language, value) VALUE (%s,%s,%s);', (_text, _to, _dst))
                conn.commit()
            else:
                raise TransError(json['error_msg'])
        return _dst

    def close(self):
        self.conn.close()


def get_default_translate():
    return Translate('20180920000210032', 'MzP5pEEZV_QorZcHS2JF')


if __name__ == '__main__':
    translate = get_default_translate()
    print(translate.trans('returnApplyCount'))
