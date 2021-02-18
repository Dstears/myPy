import os
import re
import sys
from xml.dom.minidom import parse
import xml.dom.minidom
import requests
import xlwt
import subprocess


class Pom(object):
    def __init__(self, path):
        self.path = path
        parse = xml.dom.minidom.parse(path)
        root = parse.documentElement
        artifacts = root.getElementsByTagName('artifactId')
        for artifact in artifacts:
            if artifact.parentNode.tagName == 'project':
                self.module_name = artifact.firstChild.data


class Dependency(object):
    def __init__(self, group_id, artifact_id, version, module):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.module = module

    def __str__(self):
        return self.group_id + ':' + self.artifact_id + ':' + self.version + '(' + self.module + ')'

    def equals(self, target):
        return self.group_id == target.group_id and self.artifact_id == target.artifact_id and self.version == target.version


def search_pom(path):
    result_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('pom.xml'):
                result_list.append(Pom(file_path))
    return result_list


def read_file(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            join = os.path.join(root, file)
            if join.endswith('txt'):
                with open(join, 'r') as r:
                    read = r.read()
                    split = read.split('\n')
                    for _i in split:
                        findall = re.findall('^[^a-zA-Z]*', _i)
                        _i = _i.replace(findall[0], '')
                        if _i.strip() != '':
                            i_split = _i.split(':')
                            dependency = Dependency(i_split[0], i_split[1], i_split[3], file.replace('.txt', ''))
                            yield dependency


if __name__ == '__main__':
    code_path = '/Users/wangxiaolei/Documents/ody/code/baseline/web/ouser'
    settings_xml = '/Users/wangxiaolei/Documents/ody/mvn/2.9.6/settings.xml'
    current_file_path = '/Users/wangxiaolei/Documents/code/workspace/maven'
    mvn_cmd = 'mvn'
    run_cmd = True
    district = True
    warehouse_list = [
        {'name': 'aliyun', 'path': 'https://maven.aliyun.com/nexus/content/groups/public/',
         'func': lambda text, dependency: text.__contains__(dependency.artifact_id)},
        {'name': 'maven', 'path': 'https://repo.maven.apache.org/maven2/',
         'func': lambda text, dependency: text.__contains__(dependency.artifact_id)}
    ]

    if run_cmd:
        poms = search_pom(code_path)
        size = poms.__len__()
        print('需要执行mvn tree，一共发现%s个pom.xml文件' % size)
        run_index = 1
        for i in poms:
            cmd = [mvn_cmd, 'dependency:tree', '-s', settings_xml, '-D',
                   'outputFile=' + current_file_path + '/' + i.module_name + '.txt', '-f', i.path]
            print('开始执行第 %s/%s 个，命令为 %s' % (run_index, size, cmd))
            subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            print('第 %s/%s 个执行成功！' % (run_index, size))
            run_index = run_index + 1
        print('mvn tree全部执行完成！')

    dependency_list = []
    for i in read_file(current_file_path):
        if district:
            has_in = False
            for j in dependency_list:
                if j.equals(i):
                    has_in = True
                    break
            if not has_in:
                dependency_list.append(i)
        else:
            dependency_list.append(i)
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet')

    row = 1
    sheet.write(0, 0, 'groupId')
    sheet.write(0, 1, 'artifactId')
    sheet.write(0, 2, 'version')
    sheet.write(0, 3, '是否自建')
    sheet.write(0, 4, '哪个module引用的')
    sheet.write(0, 5, '在哪个仓库找到')

    total = dependency_list.__len__()
    print('一共有%s个依赖需要处理' % total)

    self_build = 0
    global_build = 0

    for i in dependency_list:
        full_url = '/'.join(i.group_id.split(
            '.')) + '/' + i.artifact_id + '/' + i.version + '/' + i.artifact_id + '-' + i.version + '.pom'
        exist = False
        for j in warehouse_list:
            real_path = j['path'] + full_url
            exist = j['func'](requests.get(real_path).text, i)
            if exist:
                sheet.write(row, 0, i.group_id)
                sheet.write(row, 1, i.artifact_id)
                sheet.write(row, 2, i.version)
                sheet.write(row, 3, 'false')
                if district:
                    sheet.write(row, 4, i.module)
                    sheet.write(row, 5, j['name'])
                else:
                    sheet.write(row, 4, j['name'])
                row = row + 1
                global_build = global_build + 1
                break
        if not exist:
            sheet.write(row, 0, i.group_id)
            sheet.write(row, 1, i.artifact_id)
            sheet.write(row, 2, i.version)
            sheet.write(row, 3, 'true')
            if district:
                sheet.write(row, 4, i.module)
            row = row + 1
            self_build = self_build + 1
        print('目前处理进度%s/%s，其中自建的%s个，公共的%s个' % (self_build + global_build, total, self_build, global_build))
    print('处理完成，开始保存excel')
    workbook.save('./dependency.xls')
    print('excel保存成功！')
