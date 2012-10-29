"""This module defines the Site repository. Packages are installed into this
repository manually. All folders under the Site folder are interpreted as
packages."""

from glob import glob
from os.path import join, exists, basename
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
            a_location: pkg_path
        })
        yield pkg


def get_project(pkg_path):
    name = basename(pkg_path)
    path = join(pkg_path, 'package.py')
    if exists(path):
        id = 'site.' + name
        mod = sys.modules.get(id)
        if not mod:
            mod = imp.load_source(id, path)
        return getattr(mod, 'recipe')
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

        return prj


repository.register('site', 'Site', get_packages)
