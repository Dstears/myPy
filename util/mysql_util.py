import pymysql


def get_conn():
    return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='buxing123', db='wxl', charset='utf8')
