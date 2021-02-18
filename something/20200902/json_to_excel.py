import xlwt
import json
import re

workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet('sheet')
row = 1
sheet.write(0, 0, 'url')
sheet.write(0, 1, 'method')
sheet.write(0, 2, 'responseType')
sheet.write(0, 3, 'showError')
with open('/Users/wangxiaolei/Documents/my/python/workspace/something/20200902/pos2.0-all-ajax.json', 'r') as r:
    loads = json.load(r)
    for i in loads:
        i_ = loads[i]
        for j in i_:
            j_ = i_[j]
            print(j_)
            sheet.write(row, 0, j_['url'])
            sheet.write(row, 1, j_['method'])
            if 'responseType' in j_:
                sheet.write(row, 2, j_['responseType'])
            sheet.write(row, 3, j_['showError'])
            row = row + 1
# for i in loads:
#     url = i
#     values = loads[i]
#     for j in values:
#         if j is not None:
#             value = j
#             pre = None
#             if value.startswith('/api'):
#                 pre = re.finditer('(?<=/)api/[^/]*(?=/)', value).__next__().group()
#             else:
#                 pre = re.finditer('(?<=/)[^/]*(?=/)', value).__next__().group()
#             sheet.write(row, 0, url)
#             sheet.write(row, 1, pre)
#             sheet.write(row, 2, value)
#             row = row + 1
workbook.save('./url.xls')
