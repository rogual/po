from os.path import join
import subprocess
import shutil

import simple
import standard

url = (
    "http://www.iro.umontreal.ca/~gambit/download/"
    "gambit/v4.6/source/gambc-v4_6_6-devel.tgz"
)

# Add missing lines to get the thing to compile
patch = """
102a103,107
> %COMP_LIB% _asm.c
> %COMP_LIB% _assert.c
> %COMP_LIB% _codegen.c
> %COMP_LIB% _t-univ.c
> %COMP_LIB% _x86.c
106c111
< cl -Fegsc.exe ..\lib\libgambc.lib _host.obj _utils.obj _source.obj \
_parms.obj _env.obj _ptree1.obj _ptree2.obj _gvm.obj _back.obj _front.obj \
_prims.obj _t-c-1.obj _t-c-2.obj _t-c-3.obj _gsclib.obj _gambcgsc.obj \
_gsc.obj _gsc_.obj Kernel32.Lib User32.Lib Gdi32.Lib WS2_32.Lib
---
> cl -Fegsc.exe ..\lib\libgambc.lib _host.obj _utils.obj _source.obj \
_parms.obj _env.obj _ptree1.obj _ptree2.obj _gvm.obj _back.obj _front.obj \
_prims.obj _t-c-1.obj _t-c-2.obj _t-c-3.obj _gsclib.obj _gambcgsc.obj \
_asm.obj _assert.obj _codegen.obj _t-univ.obj _x86.obj _gsc.obj _gsc_.obj \
Kernel32.Lib User32.Lib Gdi32.Lib WS2_32.Lib
"""


@simple.source('gambit', 'Gambit Scheme', url)
def recipe(package):
    cwd = package[standard.a_location]

    build_bat = join(cwd, 'misc', 'vcexpress.bat')
    cmd = 'patch "%s"' % build_bat
    p = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE, shell=True)
    p.communicate(input=patch)
    if p.poll():
        raise Exception
    
    cmd = join('misc', 'vcexpress.bat')
    ret = subprocess.call(cmd, cwd=cwd, shell=True)
    if ret:
        raise Exception

    shutil.move(join(cwd, 'gsc', 'gsc.exe'), join(cwd, 'bin'))
    shutil.move(join(cwd, 'gsi', 'gsi.exe'), join(cwd, 'bin'))
