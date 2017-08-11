import operator
import os
import sys
import hashlib
from functools import reduce


def get_md5_sum(file_name):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()
        return hashlib.md5(data).hexdigest() + '\t' + file_name + '\n'


def write_md5_sum(file_name, md5_store_file):
    os.makedirs(os.path.dirname(md5_store_file), exist_ok=True)
    line = get_md5_sum(file_name)
    if (os.path.exists(md5_store_file)):
        open(md5_store_file, 'a').write(line)
    else:
        open(md5_store_file, 'w+').write(line)


def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value


def rm_in_dict(branch, keys):
    if len(keys) > 1:
        empty = rm_in_dict(branch[keys[0]], keys[1:])
        if empty:
            del branch[keys[0]]
    else:
        del branch[keys[0]]
    return len(branch) == 0


def add_keys(d, l, c=None):
    if len(l) > 1:
        d[l[0]] = _d = {}
        d[l[0]] = d.get(l[0], {})
        add_keys(d[l[0]], l[1:], c)
    else:
        d[l[0]] = c


def check_string_in_file(file_name, string):
    found = False
    with open(file_name) as f:
        for line in f:
            if string in line:  # Key line: check if `w` is in the line.
                found = True
    return found


def diff_files(file1, file2):
    result = list()
    with open(file1) as f1:
        with open(file2) as f2:
            lines_file_1 = f1.readlines()
            lines_file_2 = f2.readlines()
            diff = [x for x in lines_file_1 if x not in lines_file_2]
            for x in diff:
                file_name = x.split('\t')[1].replace('\n', '')
                result.append(file_name)
            return result


def safe_remove(file_name):
    try:
        os.remove(file_name)
    except IOError:
        pass


def get_file_list(dir):
    file_list = list()
    for root, subdirs, files in os.walk(dir):
        for f in files:
            file_list.append(os.path.join(root, f))
    return file_list


def get_tenant_dir(tenant):
    return os.getenv("HOME") + "/.appflow/tenant/" + tenant + "/"


def get_tenant_env_dir(tenant, env):
    return os.getenv("HOME") + "/.appflow/tenant/" + tenant + "/" + env


def get_vault_file(tenant, env):
    return os.getenv("HOME") + "/.appflow/vault/" + tenant + "/" + env


def get_md5_folder(tenant):
    return os.getenv("HOME") + "/.appflow/tmp/.appflow-" + os.getenv("USER") + "/" + tenant


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")