from os.path import join, exists
import _winreg as winreg

import system
import package
import project
import environment

recipe = project.Project('msvs', "Microsoft Visual Studio")

a_version = package.attribute('msvs.version', 'Version')
a_location = package.attribute('msvs.location', 'Location')

@system.scan.implement(recipe)
def scan(project):
    return [
        package.Package(project, {
            a_version: version,
            a_location: path
        })
        for version, path in get_installations()
    ]


@environment.initializers.implement(recipe)
def init(package):
    return [join(package[a_location], 'VC', 'bin', 'vcvars32')]


def get_installations():
    """Returns a list of (version, path) pairs for VS installations."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            '\\'.join(('SOFTWARE', 'Wow6432Node', 'Microsoft', 'VisualStudio'))
        )
    except WindowsError:
        return {}

    versions = []
    try:
        i = 0
        while True:
            try:
                version = winreg.EnumKey(key, i)
            except WindowsError:
                break

            i += 1

            try:
                sub = '\\'.join((version, 'Setup', 'VS'))
                with winreg.OpenKey(key, sub) as subkey:
                    path, type = winreg.QueryValueEx(subkey, "ProductDir")
                    versions.append((version, path))
            except WindowsError:
                continue
    finally:
        key.Close()

    return versions
