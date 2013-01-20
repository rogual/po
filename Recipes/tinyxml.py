from os.path import join

import environment
import standard
import simple
import util

url = 'http://downloads.sourceforge.net/project/' \
      'tinyxml/tinyxml/2.6.2/tinyxml_2_6_2.zip'


@simple.source('tinyxml', 'TinyXML', url)
def recipe(package):
    cwd = package[standard.a_location]
    modules = 'tinyxml tinystr tinyxmlparser tinyxmlerror'.split()
    files = lambda ext: ' '.join('.'.join((m, ext)) for m in modules)
    util.run('cl /Zi /nologo /c %s /MD' % files('cpp'), cwd=cwd)
    util.run('lib /nologo %s' % files('obj'), cwd=cwd)


environment.define_paths(recipe, {
    environment.headers: '.',
    environment.libraries: '.'
})
