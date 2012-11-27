import pickle
import contextlib
import package
import recipe
import local

from os.path import exists
from collections import defaultdict

def read(path):
    r = defaultdict(list)
    if exists(path):
        with open(path, 'rb') as catalogue_file:
            for blob in pickle.load(catalogue_file):
                pkg = load_package(blob)
                r[pkg.project.id].append(pkg)

    return r


def write(path, catalogue):
    blobs = []
    for packages in catalogue.values():
        blobs.extend(map(dump_package, packages))
    with open(path, 'wb') as catalogue_file:
        pickle.dump(blobs, catalogue_file)


@contextlib.contextmanager
def modify(path):
    contents = read(path)
    yield contents
    write(path, contents)


def dump_package(package):
    return (package.project.namespace, package.project.id, package.attributes)


def load_package(blob):
    try:
        namespace, id, attrs = blob
    except:
        id, attrs = blob
        namespace = ''
    if namespace == '':
        return package.Package(recipe.get_project(id), attrs)
    elif namespace == 'site':
        pkg = local.get_package(id)
        return pkg
    else:
        raise Exception("Bad namespace '%s'" % namespace)




