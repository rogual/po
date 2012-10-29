from os.path import join

import simple
import environment
import standard
import subprocess

url = "http://sourceforge.net/projects/" \
      "scons/files/scons/2.2.0/scons-2.2.0.tar.gz"

recipe = simple.simple('scons', "SCons", url)


@environment.executables.implement(recipe)
def bin(package):
    return [join(package[standard.a_location], 'Scripts')]


@environment.pythonpath.implement(recipe)
def pypath(package):
    return [join(
        package[standard.a_location], 'Lib', 'site-packages', 'scons-2.2.0'
    )]


@standard.installer.implement(recipe)
def do_install(package):
    path = simple.download_and_extract(url, package)
    ret = subprocess.call(
        'python setup.py install --prefix=%s' % path,
        shell=True,
        cwd=path
    )
    if ret:
        raise Exception
