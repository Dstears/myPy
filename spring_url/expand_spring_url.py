import util
import re

files = util.list_file(
    '/Users/wangxiaolei/Documents/ody/code/baseline/web/ouser/2.9.6/ouser-starter-web/src/main/java/com/odianyun/user/web',
    '.java')

for file in files:
    with open(file, 'r') as r:
        content = r.read()
        finditer = re.finditer('@RequestMapping\("[^"]*"\)', content)
        try:
            request_mapping = finditer.__next__().group()
            content = content.replace(request_mapping, '')
            finditer = re.finditer('(?<=")[^"]*(?=")', request_mapping)
            pre = finditer.__next__().group()
            if not pre.startswith('/'):
                pre = '/' + pre
            if pre.endswith('/'):
                pre = pre[:pre.__len__() - 1]
            mappings = re.findall('@PostMapping\([^)]*\)', content)

            for mapping in mappings:
                finditer = re.finditer('(?<=")[^"]*(?=")', mapping)
                url = finditer.__next__().group()
                if not url.startswith('/'):
                    url = '/' + url
                content = content.replace(mapping, '@PostMapping(value = "' + pre + url + '")')

            mappings = re.findall('@GetMapping\([^)]*\)', content)

            for mapping in mappings:
                finditer = re.finditer('(?<=")[^"]*(?=")', mapping)
                url = finditer.__next__().group()
                if not url.startswith('/'):
                    url = '/' + url
                content = content.replace(mapping, '@GetMapping(value = "' + pre + url + '")')

            mappings = re.findall(
                '@RequestMapping\(value\s=\s\"[^"]*\"',
                content)
            for mapping in mappings:
                finditer = re.finditer('(?<=")[^"]*(?=")', mapping)
                url = finditer.__next__().group()
                if not url.startswith('/'):
                    url = '/' + url
                content = content.replace(mapping, '@RequestMapping(value = "' + pre + url + '"')

            with open(file, 'w') as w:
                w.write(content)
                w.flush()
                w.close()
        except StopIteration:
            print(file)
