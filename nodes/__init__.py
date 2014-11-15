import os
from collections import defaultdict

nodes_dir = os.path.dirname(__file__)


def list_only_valid_files_in_nodes_dir(nodes_dir):
    '''
    collects all folders and files inside the nodes
    folder and sticks them into a dict
    '''

    support_dict = defaultdict(list)
    for path, subdirs, files in os.walk(nodes_dir):
        for name in files:
            if name.startswith('__'):
                continue
            if name.endswith('.pyc'):
                continue
            fullpath = os.path.join(path, name)
            directory_path = os.path.dirname(fullpath)
            directory_name = os.path.basename(directory_path)
            support_dict[directory_name].append(name[:-3])
    return support_dict

nodes_dict = list_only_valid_files_in_nodes_dir(nodes_dir)
