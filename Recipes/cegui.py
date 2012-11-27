from os.path import join, exists
import os

import simple
import standard
import environment
import util

hg_repo = 'http://crayzedsgui.hg.sourceforge.net/hgroot/crayzedsgui/cegui_mk2'

@simple.source('cegui', "Crazy Eddie's GUI")
def recipe(package):
    path = package[standard.a_location]
    #if exists(path):
    #    print 'Removing old files...'
    #    util.rmtree(path)

    #util.run('hg clone %s "%s"' % (hg_repo, path))

    build = join(path, 'build')
    if exists(build):
        print 'Removing build dir...'
        util.rmtree(build)
    os.makedirs(build)

    options = [
        ('CEGUI_BUILD_XMLPARSER_TINYXML', '1'),
        ('CMAKE_INCLUDE_PATH', '%INCLUDE%'),
        ('CMAKE_LIBRARY_PATH', '%LIB%')
    ]

    options = ' '.join('-D %s=%s' % (k, v) for k, v in options)

    util.run('cmake -G"NMake Makefiles" %s ..' % options, cwd=build)

    raise Exception


@environment.headers.implement(recipe)
def find_headers(package):
    return [join(package[standard.a_location], 'cegui', 'include')]
