from os.path import join
import subprocess

import simple
import environment
import standard

url = "http://downloads.sourceforge.net/project/" \
      "boost/boost/1.51.0/boost_1_51_0.tar.bz2"

@simple.source('boost', "Boost C++ Libraries", url, prefix='./boost_1_51_0')
def recipe(package):
    cwd = package[standard.a_location]
    ret = subprocess.call(
        '"%s"' % join(cwd, 'bootstrap.bat'), cwd=cwd, shell=True)
    if ret:
        raise Exception

    ret = subprocess.call(
        '"%s" --with-filesystem --with-thread --with-signals' % join(cwd, 'b2'),
        cwd=cwd, shell=True)
    if ret:
        raise Exception

@environment.headers.implement(recipe)
def find_headers(package):
    return [package[standard.a_location]]

@environment.libraries.implement(recipe)
def find_libraries(package):
    return [join(package[standard.a_location], 'stage', 'lib')]
