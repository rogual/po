from os.path import join

import subprocess

import environment
import standard
import simple

url = "http://zlib.net/zlib-1.2.7.tar.bz2"

@simple.source('zlib', 'Zlib', url)
def recipe(package):
    loc = package[standard.a_location]

    sln = join(loc, 'contrib', 'vstudio', 'vc10', 'zlibvc.sln')

    opts = '/p:Configuration=Release /p:Platform=Win32'
    ret = subprocess.call('msbuild %s "%s"' % (opts, sln), shell=True, cwd=loc)

    if ret:
        raise Exception


@environment.headers.implement(recipe)
def include(package):
    return [package[standard.a_location]]


@environment.libraries.implement(recipe)
def lib(package):
    loc  = package[standard.a_location]
    base = join(loc, 'contrib', 'vstudio', 'vc10', 'x86')
    return [join(base, 'ZlibDllRelease'), join(base, 'ZlibStatRelease')]
