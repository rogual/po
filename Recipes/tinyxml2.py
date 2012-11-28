from os.path import join, exists
import os

import simple
import environment
import attributes
import util

git_repo = 'https://github.com/leethomason/tinyxml2'

@simple.source('tinyxml2', "TinyXML 2")
def recipe(package):
    path = package[attributes.a_location]
    if exists(path):
        print 'Removing old files...'
        util.rmtree(path)

    util.run('git clone %s "%s"' % (git_repo, path))

    build = join(path, 'build')
    if exists(build):
        print 'Removing build dir...'
        util.rmtree(build)
    os.makedirs(build)

    options = ' '.join('-D %s=%s' % (k, v) for k, v in [
    ])

    util.run('cmake -G"NMake Makefiles" %s ..' % options, cwd=build)
    util.run('nmake tinyxml2static', cwd=build)

@environment.headers.implement(recipe)
def find(package):
    return [package[attributes.a_location]]

@environment.libraries.implement(recipe)
def find(package):
    return [join(package[attributes.a_location], 'build')]
