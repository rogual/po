import package
import standard

a_format = package.attribute('format', 'Format')
a_provenance = package.attribute('provenance', 'Provenance')
a_compiler = package.attribute('compiler', 'Compiler')

def get_default_compiler():
    return 'msvs'

