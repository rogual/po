from os.path import join, exists

import simple
import standard
import subprocess
import environment

url = "https://bullet.googlecode.com/files/bullet-2.81-rev2613.tgz"

@simple.source('bullet', 'Bullet Physics', url)
def recipe(package):
    loc = package[standard.a_location]

    sln = join(loc, 'build', 'vs2010', '0BulletSolution.sln')

    if not exists(sln):
        bat = join(loc, 'build', 'vs2010.bat')
        ret = subprocess.call(bat, shell=True, cwd=join(loc, 'build'))

    opts = '/p:Configuration=Release'
    ret = subprocess.call('msbuild %s "%s"' % (opts, sln), shell=True, cwd=loc)

    if ret:
        raise Exception


@environment.headers.implement(recipe)
def include(package):
    return [join(package[standard.a_location], 'src')]
