import util
import re
import os

import platform


class ClassFile(object):
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as _f:
            _content = _f.read()
            try:
                pa = re.finditer('(?<=package)\s+[a-zA-Z.]*\s?(?=;)', _content).__next__()
            except StopIteration:
                raise Exception(path)
            end = path.rindex('.')
            if platform.system().lower() == 'windows':
                start = path.rindex('\\')
            else:
                start = path.rindex('/')
            self.dir_path = self.path[:start]
            self.package_name = pa.group().strip()
            self.file_name = path[start + 1:end]
            self.class_name = self.package_name + '.' + self.file_name
        self.is_used = False


if __name__ == '__main__':
    # 是否是预览模式，如果关闭则直接删除文件
    preview = False
    # 需要检查的POJO里java文件目录，只支持检查POJO，轻易不要尝试检查其他的类。。。
    dto_path = '/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/promotion-model/src/main'
    # 需要检查POJO在哪些目录的java和xml文件里是否引用
    target_paths = [
        '/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/promotion-model/src/main',
        '/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/promotion-dao/src/main',
        '/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/promotion-business/src/main',
        '/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/basics-promotion-service/src/main',
        '/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/back-promotion-web/src/main'
    ]

    logger = util.get_logger('find_class_used')
    logger.debug('开始运行')
    class_list = []
    files = util.list_file(dto_path,
                           '.java')
    for i in files:
        class_list.append(ClassFile(i))
    logger.debug('找到 %s 个文件需要查找引用' % class_list.__len__())

    files = util.list_file(
        paths=target_paths
        , patterns=['.java', '.xml'])
    for i in files:
        logger.info('开始在文件 %s 中查找' % i)
        with open(i, 'r') as f:
            content = f.read()
            for j in class_list:
                logger.debug('开始查找 class: %s' % j.class_name)
                # 首先最简单的，判断是否有全路径名引入
                if content.__contains__(j.class_name) > 0:
                    logger.info('class： %s 找到直接引用' % j.class_name)
                    j.is_used = True
                # 判断当前文件是否在相同路径下
                if i.__contains__(j.dir_path) and i != j.path:
                    if content.__contains__(j.file_name) > 0:
                        logger.info('class： %s 找到同目录引用' % j.class_name)
                        j.is_used = True
                # 判断是否import了所有文件
                name___ = j.package_name + '.*'
                if content.__contains__(name___):
                    if content.__contains__(j.file_name):
                        logger.info('class： %s 找到了*引用' % j.class_name)
                        j.is_used = True
    for i in class_list:
        if not i.is_used:
            if preview:
                print(i)
            else:
                os.remove(i.path)
