import json
from os.path import join, getctime
import os

def newest(path_to_dir):
    """
    Returns the most recently created file in a directory
    """
    path_to_dir = join(os.getcwd(), path_to_dir)
    files = os.listdir(path_to_dir)
    paths = [os.path.join(path_to_dir, basename) for basename in files]
    return max(paths, key=getctime)


def open_recent_data():
    """
    Returns the most recent data and header
    """
    with open(newest('JSON'), encoding='utf-8') as f:
        data = json.loads(f.read())
        header = data['header']
        data.pop('header', None)
    return (data, header)
