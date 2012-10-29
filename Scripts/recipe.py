from os.path import join, exists, splitext, basename
from glob import glob

import imp
import sys

import paths

def load(name):
    """Load and return the named recipe if it exists, otherwise return None."""
    path = join(paths.recipes, name + '.py')
    if exists(path):
        id = 'recipe.' + name
        mod = sys.modules.get(id)
        if not mod:
            mod = imp.load_source(id, path)
        return mod


def get_project(project_id):
    rcp = load(project_id)
    if rcp:
        return rcp.recipe

def get_projects():
    for path in glob(join(paths.recipes, '*.py')):
        yield get_project(splitext(basename(path))[0])

def get_list(interface):
    result = []
    for project in get_projects():
        result.extend(interface(project))
    return result

