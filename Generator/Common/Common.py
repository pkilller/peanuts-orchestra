import re
import subprocess
import time
import hashlib
import os


def md5(content):
    m1 = hashlib.md5()
    m1.update(content)
    return m1.hexdigest()


def __gen_cache_path(group, id):
    file_name = group + '_' + md5(id)
    return './cache/%s' % file_name

"""
def check_cache(group, id):
    cache_path = __gen_cache_path(id)
    return os.path.exists(cache_path)


def rename_cache(old_id, new_id):
    try:
        old_path = __gen_cache_path(old_id)
        new_path = __gen_cache_path(new_id)
        if check_cache(old_id):
            os.rename(old_path, new_path)
    except:
        print('rename_cache(%s, %s) err~' % (old_path, new_path))
        pass
"""


def read_cache(group, id):
    cache_path = __gen_cache_path(group, id)
    try:
        file = open(cache_path, 'r')
        data = file.read()
        file.close()
        return data
    except:
        return None


def write_cache(group, id, content):
    pache_path = __gen_cache_path(group, id)
    try:
        file = open(pache_path, 'w+')
        file.write(content)
        file.close()
        return True
    except Exception, e:
        return False


def get_subs(path, partten='*'):
    ret_code, out, err = exec_cmd(cwd=path, cmdline='find -iname "%s"' % partten)
    if ret_code != 0:
        return None
    return out.split('\n')


# return : (ret_code, normal, error) or (None, None, None)
def exec_cmd(cmdline, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    try:
        subp = subprocess.Popen(cmdline, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception, e:
        print(str(e))
        return None, None, None
    out, err = subp.communicate()
    normal = None
    error = None
    # if out:
    #     normal = out.decode(errors='ignore', encoding='UTF-8')
    normal = out
    if err:
        error = err.decode()
    return subp.returncode, normal, error


def read_file(path):
    try:
        file = open(path, 'r')
        data = file.read()
        file.close()
        return data
    except:
        return None



