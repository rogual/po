from os.path import exists, join
from os import makedirs

import project
import package
import download
import standard
import environment
import paths
import compile
import util


def simple(id, name, url, prefix=None):
    """Shortcut for defining simple packages. A simple package is one that can
    be downloaded, extracted and used as-is. Executables are assumed to be
    in standard unix places if they exist."""
    recipe = project.Project(id, name)

    @standard.factory.implement(recipe)
    def do_find(project, specifier):
        pkg = package.Package(recipe)
        if specifier.match(pkg):
            return pkg

    @standard.installer.implement(recipe)
    def do_install(package):
        download_and_extract(url, package, prefix)

    @standard.uninstaller.implement(recipe)
    def do_uninstall(package):
        loc = package[standard.a_location]
        if exists(loc):
            util.rmtree(package[standard.a_location])

    # Add standard locations to environment paths

    def implement_paths(interface, paths):
        @interface.implement(recipe)
        def find_paths(package):
            loc = package[standard.a_location]
            return list(filter(exists, (join(loc, path) for path in paths)))

    env = {
        environment.executables: [
            'bin',
            'wbin',
            join('usr', 'local', 'bin'),
            join('usr', 'local', 'wbin')
        ],
        environment.headers: ['include'],
        environment.libraries: ['lib']
    }

    for interface, paths in env.items():
        implement_paths(interface, paths)

    return recipe


def source(id, name, url=None, prefix=None):
    """Shortcut for defining source packages. These packages contain source
    code that needs to be compiled."""

    project = simple(id, name, url, prefix)

    @standard.factory.implement(project)
    def factory(project, specifier):
        format = specifier.get(compile.a_format, 'binary')
        if format not in ['source', 'binary']:
            return "Invalid format."

        provenance = specifier.get(compile.a_provenance, 'compiled')
        if provenance not in ['compiled']:
            return "Source-only distribution."

        compiler = specifier.get(compile.a_compiler)
        if not compiler:
            compiler = compile.get_default_compiler()

        return package.Package(project, {
            compile.a_format: format,
            compile.a_provenance: provenance,
            compile.a_compiler: compiler
        })

    install_fn = [lambda pkg: None]

    @standard.installer.implement(project)
    def install(package):
        if url:
            download_and_extract(url, package, prefix)
        install_fn[0](package)

    def deco(fn):
        install_fn[0] = fn
        return project

    return deco


def download_and_extract(url, package, prefix=None):
    cache_path = join(paths.cache, package.project.id)
    if not exists(cache_path):
        makedirs(cache_path)
    path = download.url_filename(url)
    path = join(cache_path, path)

    if not exists(path):
        download.download(url, path)

    dest = package[standard.a_location]

    if exists(dest):
        print 'DEBUG'; return dest
        print 'Removing old files...'
        util.rmtree(dest)

    print 'Extracting...'
    download.extract(path, dest, prefix)
    return dest
