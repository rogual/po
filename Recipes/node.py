from os.path import join
import subprocess
import shutil

import simple
import standard

url = "http://nodejs.org/dist/v0.8.19/node-v0.8.19.tar.gz"


@simple.source('node', 'Node.js', url)
def recipe(package):
    cwd = package[standard.a_location]
    build_bat = join(cwd, 'vcbuild.bat')
    patch_by_replacing(build_bat, 'msvs_version=2010', 'msvs_version=2012')
    ret = subprocess.call(build_bat, cwd=cwd, shell=True)
    if ret:
        raise Exception


def patch_by_replacing(fname, old, new):
    with open(fname) as f:
        text = f.read()
    text = text.replace(old, new)
    with open(fname, 'wt') as f:
        f.write(text)
