import git
import os

git_path = 'git@git.odianyun.local:baseline/war/oms-api.git'
git_version = '2.9.6'

detail_path = git_path.replace('git@git.odianyun.local:', '').replace('.git', '')

pre_path = '/Users/wangxiaolei/Documents/ody/code/'

project_name = detail_path[detail_path.rindex('/') + 1:]

real_path = pre_path + detail_path + '/' + str(git_version)

if not os.path.exists(real_path):
    os.makedirs(real_path)

try:
    repo = git.Repo(real_path)
except git.InvalidGitRepositoryError:
    repo = git.Repo.clone_from(url=git_path, to_path=real_path)

if git_version != 'master':
    tag_name = project_name + git_version
else:
    tag_name = git_version
try:
    if not repo.git.branch().__contains__(git_version):
        repo.git.checkout(tag_name)
except Exception:
    pass
print('done')