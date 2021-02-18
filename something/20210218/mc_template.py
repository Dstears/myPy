import util
import xlwt

if __name__ == '__main__':
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet1')
    get = util.HttpPostJson('http://odianyun.com/open-api/mcTemplate/queryMcTemplateList.do?UserId=442')
    get.add_param('currentPage', 1)
    get.add_param('itemsPerPage', 9999)
    get.add_param('obj', {})
    get.execute()
    json = get.get_json()
    sheet.write(0, 0, '模板名称')
    sheet.write(0, 1, '模板编码')
    sheet.write(0, 2, '模板内容')
    index = 1
    for i in json['data']['data']['listObj']:
        sheet.write(index, 0, i['templateName'])
        sheet.write(index, 1, i['templateCode'])
        sheet.write(index, 2, i['msgContent'])
        index = index + 1
    workbook.save('mcTemplate.xls')
