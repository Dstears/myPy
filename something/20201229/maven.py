import os

if __name__ == '__main__':
    path = '/Users/wangxiaolei/Documents/ody/code/2.9.6'
    dirs = os.listdir(path)
    for _dir in dirs:
        full_path = os.path.join(path, _dir)
        if os.path.isdir(full_path):
            os.system('mvn clean -s /Users/wangxiaolei/Documents/ody/mvn/2.9.6/settings.xml -f ' + full_path + '/pom.xml')
