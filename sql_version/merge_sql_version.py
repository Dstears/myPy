import os


def filter_not_start_with_point(name):
    return not name.startswith('.')


def ignore_name(name):
    return name not in ignore_names


def in_versions(name):
    return name <= version


if __name__ == '__main__':

    sql_path = '/Users/wangxiaolei/Documents/ody/sql'
    # 合成版本小于等于设置版本的sql
    version = '2.9.6'

    sql_name = 'full.sql'

    ignore_names = ['文件夹运行顺序.txt', '脚本编写规范.txt', 'demo脚本(最后执行)', 'inner_odts(聚石塔内部库不需要刷)', 'inner_odts(聚石塔库不需要刷)',
                    '造数据脚本']

    with open(sql_name, 'w') as w:

        for i in sorted(
                filter(lambda name: in_versions(name) and filter_not_start_with_point(name), os.listdir(sql_path))):
            for j in sorted(filter(lambda name: filter_not_start_with_point(name) and ignore_name(name),
                                   os.listdir(os.path.join(sql_path, i)))):
                for k in sorted(filter(lambda name: filter_not_start_with_point(name) and ignore_name(name),
                                       os.listdir(os.path.join(os.path.join(sql_path, i), j)))):
                    for m in sorted(filter(lambda name: filter_not_start_with_point(name) and ignore_name(name),
                                           os.listdir(
                                               os.path.join(os.path.join(os.path.join(sql_path, i), j), k)))):
                        real_file_path = os.path.join(os.path.join(os.path.join(os.path.join(sql_path, i), j), k), m)
                        with open(real_file_path, 'r') as r:
                            lines = r.readlines()
                            for line in lines:
                                w.write(line.replace("ops_company_id", '2915').replace("ops_admin_name",
                                                                                       'superadmin').replace(
                                    "ops_create_username", 'superadmin').replace("ops_name_space", 'trunk').replace('﻿',
                                                                                                                    ''))
                            w.write('\n')
        w.flush()
        w.close()

    print('sudo /usr/local/Cellar/mysql\@5.7/5.7.27_1/bin/mysql.server restart')
    print('mysql -uroot -pvBs2XYChmYr]CX mysql < ' + os.path.join(os.getcwd(), 'full.sql'))
