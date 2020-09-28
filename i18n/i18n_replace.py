import util
import re

module_path = '/Users/wangxiaolei/Documents/ody/code/baseline/static/vue-static/2.9.3/src'


def find(file_path):
    with open(file_path, 'r') as r:
        content = r.read()
        # ""包围的
        for i in re.findall('[a-zA-Z]*="[^"\'>{]*[\u4e00-\u9fa5][^"\'>{]*"', content):
            print(i)


js_files = util.list_file(module_path, '.js')
vue_files = util.list_file(module_path, '.vue')

for js in js_files:
    find(js)
for vue in vue_files:
    find(vue)
