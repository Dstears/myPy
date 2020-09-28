import util
import re

logger = util.get_logger('i18n_replace')

result_: set = set([])


def load_i18n_file(file_path):
    i18n_map = {}
    with open(file_path, 'r') as r:
        content = r.read()
        for i in content.split('\n'):
            i = i.strip()
            if i.__contains__(':') and i != '':
                group = re.finditer('(?<=[\'"])\s?:\s?(?=[\'"])', i).__next__().group()
                key = i.split(group)[0].strip()
                key = key[1:key.__len__() - 1]
                value = i.split(group)[1].strip()
                value = value[1:value.__len__() - 2]
                i18n_map[key] = value
    return i18n_map


def list_i18n_key(file_path):
    with open(file_path, 'r') as r:
        content = r.read()
        for i in re.finditer('(?<=\$t\(\')[^\']*(?=\'\))', content):
            result_.add(i.group())


def trans(result):
    zh_file_path = '/Users/wangxiaolei/Documents/ody/code/baseline/static/vue-static/2.9.3/packages/lang/zh_CN.js'

    en_file_path = '/Users/wangxiaolei/Documents/ody/code/baseline/static/vue-static/2.9.3/packages/lang/en_US.js'

    translate = util.get_default_translate()

    zh_map = load_i18n_file(zh_file_path)
    en_map = load_i18n_file(en_file_path)

    for i in result:
        try:
            language = translate.language(i)
            if language == 'zh':
                if i not in en_map:
                    en_map[i] = translate.trans(i)
            else:
                if i not in zh_map:
                    zh_map[i] = translate.trans(i)
        except TypeError as e:
            logger.error(e)
            raise e
        except util.LanguageError as e:
            logger.error(e)
        except util.TransError as e:
            logger.error(e)

    translate.close()
    # with open(zh_file_path, 'w') as w:
    #     content = 'export default {'
    #     for i in zh_map:
    #         content = content + '\n\'' + i + '\': \'' + zh_map[i] + '\','
    #     content = content + '}'
    #     w.write(content)
    with open(en_file_path, 'w') as w:
        content = 'export default {'
        for i in en_map:
            content = content + '\n\'' + i + '\': \'' + en_map[i] + '\','
        content = content + '}'
        w.write(content)


if __name__ == '__main__':
    module_path = '/Users/wangxiaolei/Documents/ody/code/baseline/static/vue-static/2.9.3/src'
    vue_files = util.list_file(module_path, '.vue')
    js_files = util.list_file(module_path, '.js')

    for js in js_files:
        list_i18n_key(js)
    for vue in vue_files:
        list_i18n_key(vue)
    trans(result_)
    # api = util.MysqlApi(_host='10.10.0.31', _port=3306, _user='root', _passwd='F5ID37Q5TFAZFTJJG', _db='ouser',
    #                     _charset='utf8')
    # query_all = api.query_all('select name from u_function where type in (1,4);')
    # result_: set = set([])
    # for i in query_all:
    #     result_.add(i[0])
    # trans(result_)
