"""This module defines the Site repository. Packages are installed into this
repository manually. All folders under the Site folder are interpreted as
packages."""

from glob import glob
from os.path import join, exists, basename, normcase
import imp
import sys

import repository
import paths
import environment
import package
import project

a_location = package.attribute('site.location', 'Location')

def get_packages():
    for pkg_path in glob(join(paths.site, '*')):
        prj = get_project(pkg_path)
        pkg = package.Package(prj, {
            a_location: normcase(pkg_path)
        })
        yield pkg


def find_installed_packages(package_specifier):
    r = []
    for package in get_packages():
        if package_specifier.match(package):
            r.append(package)
    return r


def get_package(project_id):
    path = join(paths.site, project_id)
    if exists(path):
        prj = get_project(path)
        return package.Package(prj, {
            a_location: normcase(path)
        })


def get_project(pkg_path):
    name = basename(pkg_path)
    path = join(pkg_path, 'package.py')
    if exists(path):
        id = 'site.' + name
        mod = sys.modules.get(id)
        if not mod:
            mod = imp.load_source(id, path)
        prj = getattr(mod, 'recipe')
    else:
        prj = project.Project(name, name)

        def implement(interface, paths):
            @interface.implement(prj)
            def scan(pkg):
                return paths

        for interface, interface_paths in (
            (environment.executables, ['.', 'bin']),
            (environment.libraries, ['lib']),
            (environment.headers, ['include'])
        ):
            # Don't clobber custom ones
            if prj not in interface.impl:
                subs = [join(pkg_path, ipath) for ipath in interface_paths]
                rels = [join(sub, 'release') for sub in subs]
                subs.extend(rels)
                implement(interface, filter(exists, subs))

    prj.namespace = 'site'
    return prj


repository.register('site', 'Site', get_packages, find_installed_packages)
