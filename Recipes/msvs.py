from os.path import join, exists
import _winreg as winreg

import system
import package
import project
import standard
import attributes
import environment

recipe = project.Project('msvs', "Microsoft Visual Studio")

a_version = attributes.a_version
a_location = attributes.a_location

downloads = {
    '9.0': 'http://www.microsoft.com/en-gb/download/details.aspx?id=3D20682'
}


@standard.factory.implement(recipe)
def factory(project, specifier):
    version = specifier.get(a_version, max(downloads.keys()))
    pkg = package.Package(recipe, {a_version: version})
    if specifier.match(pkg):
        return pkg


@standard.installer.implement(recipe)
def install(package):
    print 'install MSVC', package[a_version]
    raise Exception


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


@environment.executables.implement(recipe)
def find_executables(package):
    return [join(path, 'bin') for version, path in get_ctps()]


@environment.headers.implement(recipe)
def find_headers(package):
    return [join(path, 'include') for version, path in get_ctps()]


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
        for version in iterate_keys(key):
            try:
                sub = '\\'.join((version, 'Setup'))
                with winreg.OpenKey(key, sub) as subkey:
                    path, type = winreg.QueryValueEx(subkey, "Dbghelp_path")
                    suff = 'Common7\\IDE\\'
                    if path.endswith(suff):
                        path = path[:-len(suff)]
                        versions.append((version, path))
            except WindowsError:
                continue
    finally:
        key.Close()

    return versions


def get_ctps():
    """Find all installed compiler updates."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC_CTP'
        )
    except WindowsError:
        return

    try:
        for version, path, type in iterate_values(key):
            yield version, path

    finally:
        key.Close()


def iterate_keys(key):
    """Yields the name of each subkey in key"""
    i = 0
    while True:
        try:
            yield winreg.EnumKey(key, i)
        except WindowsError:
            break
        i += 1


def iterate_values(key):
    """Yields (name, value, type) for each value in the key"""
    i = 0
    while True:
        try:
            yield winreg.EnumValue(key, i)
        except WindowsError:
            break
        i += 1
