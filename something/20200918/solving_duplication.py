import util

file = util.list_file('/Users/wangxiaolei/Documents/ody/code/baseline/web/promotion/2.9.6/promotion-business', '.java')

file_names = {}
for i in file:
    file_name = i[i.rindex('/') + 1:].replace('.java', '')
    if file_name in file_names:
        count = file_names[file_name]
        count = count + 1
        file_names[file_name] = count
    else:
        file_names[file_name] = 1
index = 0
for i in file_names:
    count = file_names[i]
    if count > 1:
        print(i + '|' + str(count))
        index = index + 1
print(index)
