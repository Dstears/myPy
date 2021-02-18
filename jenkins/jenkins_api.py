import util
import xml.etree.cElementTree as ET


class JenkinsApi(object):
    def __init__(self, jenkins_path):
        self.jenkins_path = jenkins_path

    def get_jenkins_path(self):
        return self.jenkins_path

    def get_root(self):
        return JenkinsApiRoot(self)

    def get_views(self):
        return self.get_root().get_views()


class JenkinsApiRoot(object):
    def __init__(self, jenkins_api: JenkinsApi):
        self.jenkins_api = jenkins_api
        self.root = None

    def __init_root__(self):
        get = util.HttpGet(self.jenkins_api.get_jenkins_path() + 'api/json?pretty=true')
        get.execute()
        self.root = get.get_json()

    def get_root(self):
        if self.root is None:
            self.__init_root__()
        return self.root

    def get_views(self):
        return map(lambda x: JenkinsApiView(self.jenkins_api, x['name']), self.get_root()['views'])


class JenkinsApiView(object):
    def __init__(self, jenkins_api: JenkinsApi, view_name):
        self.jenkins_api = jenkins_api
        self.view = None
        self.view_name = view_name

    def __init_view__(self):
        get = util.HttpGet(self.jenkins_api.jenkins_path + '/view/' + self.view_name + '/api/json?pretty=true')
        get.execute()
        self.view = get.get_json()

    def get_view(self):
        if self.view is None:
            self.__init_view__()
        return self.view

    def get_jobs(self):
        return map(lambda x: JenkinsJob(self.jenkins_api, x['name']), self.get_view()['jobs'])


class JenkinsJob(object):
    def __init__(self, jenkins_api: JenkinsApi, job_name):
        self.jenkins_api = jenkins_api
        self.job_name = job_name
        self.job = None
        self.config = None

    def __init_job__(self):
        get = util.HttpGet(self.jenkins_api.jenkins_path + '/job/' + self.job_name + '/api/json?pretty=true')
        get.execute()
        self.job = get.get_json()

    def get_job(self):
        if self.job is None:
            self.__init_job__()
        return self.job

    def __init_config__(self):
        get = util.HttpGet(self.jenkins_api.jenkins_path + '/job/' + self.job_name + '/config.xml')
        get.execute()
        self.config = ET.fromstring(get.get_text())

    def get_config(self):
        if self.config is None:
            self.__init_config__()
        return self.config

    def get_git_info(self):
        scm = self.get_config().find('scm')
        result = {'job_name': self.job_name}
        try:
            result['url'] = scm.find('userRemoteConfigs').find('hudson.plugins.git.UserRemoteConfig').find('url').text
            result['branch'] = scm.find('branches').find('hudson.plugins.git.BranchSpec').find('name').text
        except AttributeError:
            pass
        return result


if __name__ == '__main__':
    api = JenkinsApi('http://192.168.3.162:8896/')
    root = api.get_root()
    views = api.get_views()
    for i in views:
        for j in i.get_jobs():
            info = j.get_git_info()
            if 'branch' in info:
                if info['branch'].__contains__('ddyh'):
                    print(info)
            else:
                print(info)
