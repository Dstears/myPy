import os


def list_file(path=None, pattern=None, paths=None, patterns=None):
    p = []
    pp = []
    if patterns is not None:
        for i in patterns:
            p.append(i)
    if pattern is not None:
        p.append(pattern)
    if paths is not None:
        for i in paths:
            pp.append(i)
    if path is not None:
        pp.append(path)
    for one_path in pp:
        for root, dirs, files in os.walk(one_path):
            for file in files:
                if p.__len__() > 0:
                    is_target = False
                    for i in p:
                        if file.endswith(i):
                            is_target = True
                    if is_target:
                        yield root + '/' + file
                else:
                    yield root + '/' + file
