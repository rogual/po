from os.path import abspath, dirname, join

scripts = dirname(abspath(__file__))
manager = dirname(scripts)
packages = dirname(manager)
recipes = join(manager, 'Recipes')
state = join(manager, 'State')
cache = join(manager, 'Cache')
executables = join(manager, 'Executables')

site = abspath(join(packages, '..', 'Site'))
