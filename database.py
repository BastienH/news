import json
from os.path import join, getctime
import os

def newest(path):
    path = join(path)
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=getctime)

global data
global header

with open(newest('JSON')) as f:
    data = json.loads(f.read())
    header = data['header']
    data.pop('header', None)
