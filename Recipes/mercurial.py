import sys
import subprocess

import simple
import attributes
import environment
import util

url = 'http://mercurial.selenic.com/release/mercurial-2.4.tar.gz'

@simple.source('mercurial', 'Mercurial', url)
def recipe(package):

    # Mercurial doesn't compile with 64-bit Python
    util.require_register_width(32)

    cwd = package[attributes.a_location]

    # Taken from Mercurial's Makefile
    cmd = '%s setup.py build_py -c -d . build_ext -i build_hgexe -i build_mo'
    cmd = cmd % sys.executable
    ret = util.run(cmd, shell=True, cwd=cwd)

@environment.executables.implement(recipe)
def scan(package):
    return [package[attributes.a_location]]

@environment.pythonpath.implement(recipe)
def scan(package):
    return [package[attributes.a_location]]

