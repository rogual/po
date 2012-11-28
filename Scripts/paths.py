import json

from os.path import abspath, dirname, join

scripts = dirname(abspath(__file__))
manager = dirname(scripts)
recipes = join(manager, 'Recipes')
state = join(manager, 'State')
cache = join(manager, 'Cache')
executables = join(manager, 'Executables')

settings = json.loads(open(join(state, 'settings.json')).read())
packages = settings['packages']
site = settings['site']
