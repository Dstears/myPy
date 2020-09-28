import pymysql
import util


class MysqlApi(object):

    def __init__(self, _host, _port, _user, _passwd, _db, _charset='utf8'):
        self.conn = pymysql.connect(host=_host, port=_port, user=_user, passwd=_passwd, db=_db, charset=_charset)
        self.logging = util.get_logger('MysqlApi')
        self.auto_commit = True
        self.logging.debug(
            'host：%s，port：%s，user：%s，passwd：%s，db：%s，charset：%s，auto_commit：%s' % (
                _host, _port, _user, _passwd, _db, _charset, self.auto_commit))

    def execute(self, sql, *args):
        cursor = self.conn.cursor()
        sql = cursor.mogrify(sql, *args)
        self.logging.debug('execute：%s' % sql)
        cursor.execute(sql)
        cursor.close()
        if self.auto_commit:
            self.conn.commit()

    def format_sql(self, sql, *args):
        cursor = self.conn.cursor()
        mogrify = cursor.mogrify(sql, args=args)
        cursor.close()
        return mogrify

    def query_one(self, sql, *args):
        cursor = self.conn.cursor()
        sql = cursor.mogrify(sql, *args)
        self.logging.debug('fetchone：%s' % sql)
        cursor.execute(sql)
        fetchone = cursor.fetchone()
        cursor.close()
        return fetchone

    def query_all(self, sql, *args):
        cursor = self.conn.cursor()
        sql = cursor.mogrify(sql, *args)
        self.logging.debug('fetchall：%s' % sql)
        cursor.execute(sql)
        fetchall = cursor.fetchall()
        cursor.close()
        return fetchall

    def query_many(self, sql, size, *args):
        cursor = self.conn.cursor()
        sql = cursor.mogrify(sql, *args)
        self.logging.debug('fetchmany：%s' % sql)
        cursor.execute(sql)
        fetchmany = cursor.fetchmany(size)
        cursor.close()
        return fetchmany

    def commit(self):
        self.conn.commit()

    def set_auto_commit(self, auto_commit: bool):
        self.auto_commit = auto_commit

    def close(self):
        self.conn.close()


def get_default_mysql_api():
    return MysqlApi(_host='127.0.0.1', _port=3306, _user='root', _passwd='buxing123', _db='wxl', _charset='utf8')


if __name__ == '__main__':
    api = get_default_mysql_api()
    print(api.format_sql('select `type` from str_language where str_key = %s;', 'en'))
