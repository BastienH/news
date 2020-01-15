import json
from os.path import join, getctime
import os

def newest(path):
    path = join(os.getcwd(), path)
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=getctime)


def open_recent_data():
    with open(newest('JSON')) as f:
        data = json.loads(f.read())
        header = data['header']
        data.pop('header', None)

    return (data, header)
