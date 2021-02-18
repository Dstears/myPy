import os


def filter_not_start_with_point(name):
    return not name.startswith('.')


def ignore_name(name):
    return name not in ignore_names


def in_versions(name):
    return name <= version


if __name__ == '__main__':

    sql_path = '/Users/wangxiaolei/Documents/ody/sql'
    version = '2.9.6'

    ignore_names = ['文件夹运行顺序.txt', '脚本编写规范.txt', 'demo脚本(最后执行)', 'inner_odts(聚石塔内部库不需要刷)', 'inner_odts(聚石塔库不需要刷)',
                    '造数据脚本']

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
                    content = ''
                    with open(real_file_path, 'r') as r:
                        content = r.read()
                        if '﻿' in content:
                            print(real_file_path.replace(sql_path, ''))
                        content = content.replace('﻿', '')
                        r.flush()
                    # with open(real_file_path, 'w') as w:
                    #     w.write(content)
                    #     w.flush()
