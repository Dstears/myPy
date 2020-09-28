import util


class Code(object):
    def __init__(self, one):
        self.pool = one[0]
        self.category = one[1]
        self.parent_code = one[2]
        self.code = one[3]
        self.name = one[4]
        self.data_type = one[5]
        self.language = one[6]
        self.sort = one[7]

    def get_key(self):
        return str(self.pool) + '_' + str(self.category) + '_' + str(self.parent_code) + '_' + str(
            self.code) + '-' + str(self.data_type)


mysql_api = util.MysqlApi('192.168.8.69', 3306, 'root', 'ody,123', 'misc')

query_all = mysql_api.query_all('select pool,category,parent_code,code,name,data_type,language,sort from code;')

code_map = {}

for i in query_all:
    code = Code(i)
    key = code.get_key()
    if key in code_map:
        code_list = code_map[key]
    else:
        code_list = []
    code_list.append(code)
    code_map[key] = code_list
translate = util.get_default_translate()
for i in code_map:
    code_list = code_map[i]
    if code_list.__len__() < 2:
        one = code_list[0]
        language = one.language
        name = translate.trans(one.name)
        if language == 'zh_CN':
            lan = 'en_US'
        else:
            lan = 'zh_CN'
        sql = mysql_api.format_sql(
            'insert into misc.code (pool,category,parent_code,code,name,data_type,language,sort,is_deleted,company_id) value (%s,%s,%s,%s,%s,%s,%s,%s,0,-1);' %
            ('\'' + one.pool + '\'', '\'' + one.category + '\'',
             '\'' + one.parent_code + '\'' if one.parent_code is not None else 'null', '\'' + one.code + '\'',
             '\'' + name + '\'',
             '\'' + one.data_type + '\'', '\'' + lan + '\'', one.sort))
        print(sql)

mysql_api.close()
