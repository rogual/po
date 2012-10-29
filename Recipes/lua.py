import os
from os.path import join
import subprocess

import simple
import standard
import package

url = "http://www.lua.org/ftp/lua-5.2.1.tar.gz"

@simple.source('lua', 'Lua', url)
def recipe(package):
    libsrc = """
        lapi lcode lctype ldebug ldo ldump lfunc lgc llex lmem lobject lopcodes
        lparser lstate lstring ltable ltm lundump lvm lzio lauxlib lbaselib
        lbitlib lcorolib ldblib liolib lmathlib loslib lstrlib ltablib loadlib
        linit
    """.replace('\n', '').split()

    print 'Compiling...'

    cwd = package[standard.a_location]

    os.makedirs(join(cwd, 'lib'))
    os.makedirs(join(cwd, 'obj'))
    os.makedirs(join(cwd, 'bin'))

    def compile(name):
        c = join('src', '%s.c' % name)
        o = join('obj', '%s.o' % name)
        cmd = 'cl /nologo /c /Fo%s %s' % (o, c)
        ret = subprocess.call(cmd, shell=True, cwd=cwd)
        if ret:
            raise Exception
        return o

    def build_bin(name):
        o = compile(name)
        bin = join('bin', name + '.exe')
        cmd = 'link /nologo /out:%s %s %s' % (bin, o, lib)
        ret = subprocess.call(cmd, shell=True, cwd=cwd)
        if ret:
            raise Exception
        return bin

    objs = map(compile, libsrc)

    lib = join('lib', 'lua.lib')

    cmd = 'lib /nologo /out:%s %s' % (lib, ' '.join(objs))
    ret = subprocess.call(cmd, shell=True, cwd=cwd)
    if ret:
        raise Exception

    map(build_bin, ['lua', 'luac'])
