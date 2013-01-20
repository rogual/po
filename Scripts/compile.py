import package
import standard

a_format = package.attribute('format', 'Format')
a_provenance = package.attribute('provenance', 'Provenance')
a_compiler = package.attribute('compiler', 'Compiler')
a_configuration = package.attribute('configuration', 'Configuration')

def get_default_compiler():
    return 'msvs'

