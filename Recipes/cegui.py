from os.path import join, exists
import os

import simple
import standard
import environment
import util


hg_repo = 'http://crayzedsgui.hg.sourceforge.net/hgroot/crayzedsgui/cegui_mk2'


@simple.source('cegui', "CEGUI", configurations=['release', 'debug'])
def recipe(package):
    path = package[standard.a_location]
    if exists(path):
        print 'Removing old files...'
        util.rmtree(path)

    util.run('hg clone %s "%s"' % (hg_repo, path))

    build = join(path, 'build')
    if 0:
        if exists(build):
            print 'Removing build dir...'
            util.rmtree(build)
        os.makedirs(build)

    build = join(build, 'release')
    if 0:
        if exists(build):
            print 'Removing build dir...'
            util.rmtree(build)
        os.makedirs(build)

    config = package[standard.a_configuration].title()

    options = [
        ('CEGUI_BUILD_TYPE', config),
        ('CEGUI_BUILD_XMLPARSER_TINYXML', '1'),
        ('CMAKE_INCLUDE_PATH', '%INCLUDE%'),
        ('CMAKE_LIBRARY_PATH', '%LIB%')
    ]

    options = ' '.join('-D %s=%s' % (k, v) for k, v in options)

    util.run('cmake -G"NMake Makefiles" %s ..' % options, cwd=build)
    util.run('nmake', cwd=build)

environment.define_paths(recipe, {
    environment.headers: [
        'cegui\\include',
        'cegui\\include\\cegui',
        'build\\debug\\cegui\\include',
    ],
    environment.libraries: ['build\\debug\\lib'],
    environment.executables: ['build\\debug\\bin']
})
