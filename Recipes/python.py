from os.path import join
import _winreg as winreg

import project
import package
import system
import environment
import repository

recipe = project.Project('python', "Python")

a_version = package.attribute('python.version', 'Version')
a_location = package.attribute('python.location', 'Location')


@system.scan.implement(recipe)
def scan(project):
    for version, path in get_installations().items():
        pkg = package.Package(project, {
            a_version: version,
            a_location: path
        })
        yield pkg


@environment.executables.implement(recipe)
def find_executables(package):
    loc = package[a_location]
    return [loc, join(loc, 'Scripts')]

 
@environment.headers.implement(recipe)
def find_headers(package):
    return [join(package[a_location], 'include')]

 
@environment.libraries.implement(recipe)
def find_headers(package):
    return [join(package[a_location], 'libs')]


def get_installations():
    """Returns a dictionary {ver: path} mapping installed Python version
    names to install paths."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            '\\'.join(('SOFTWARE', 'Python', 'PythonCore'))
        )
    except WindowsError:
        return {}

    pythons = {}
    try:
        i = 0
        while True:
            try:
                sub = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, sub) as subkey:
                    path = winreg.QueryValue(subkey, "InstallPath")
                    pythons[sub] = path
                i += 1
            except WindowsError:
                break
    finally:
        key.Close()

    return pythons
