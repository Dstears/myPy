import xlwt
import json
import re

workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet('sheet')
row = 1
sheet.write(0, 0, 'url')
sheet.write(0, 1, '前缀')
sheet.write(0, 2, '请求')
with open('/Users/wangxiaolei/Downloads/h5页面请求接口.json', 'r') as r:
    loads = json.load(r)
    for i in loads:
        url = i
        values = loads[i]
        for j in values:
            if j is not None:
                value = j
                pre = None
                if value.startswith('/api'):
                    pre = re.finditer('(?<=/)api/[^/]*(?=/)', value).__next__().group()
                else:
                    pre = re.finditer('(?<=/)[^/]*(?=/)', value).__next__().group()
                sheet.write(row, 0, url)
                sheet.write(row, 1, pre)
                sheet.write(row, 2, value)
                row = row + 1
workbook.save('./url.xls')
