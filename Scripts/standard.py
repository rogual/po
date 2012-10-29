"""The Standard repository holds 3rd party projects."""

from util import error
from os.path import join, exists
from os import makedirs
from collections import defaultdict

import repository
import download
import package
import recipe
import project
import paths
import pickle
import util


catalogue_path = join(paths.state, 'catalogue')

no_factory = {}

# Projects can implement these
factory = project.interface(lambda prj, spec: no_factory)
installer = project.interface()
uninstaller = project.interface()


a_location = package.attribute('location', 'Location')


@package.command()
def install(package_specifier):
    """Install a package."""
    project_id = package_specifier.project

    # Look up project.
    project = recipe.get_project(project_id)
    if not project:
        return error("No such project.")

    # Ensure not already installed.
    if find_installed_packages(package_specifier):
        return error("Already installed.")

    # Create a package representing an installed instance of the project with
    # the given parameters.
    package = factory(project, package_specifier)
    if package is no_factory:
        return error("Not installable.")
    if not package:
        return error("Invalid configuration.")
    if isinstance(package, basestring):
        return error(package)
    assert package_specifier.match(package)

    # Install to default location.
    package[a_location] = join(paths.packages, package.project.name)
    installer(package)

    # Update database.
    catalogue = read_catalogue()
    catalogue[package.project.id].append(package)
    write_catalogue(catalogue)


@package.command()
def uninstall(package_specifier):
    """Uninstall a package."""
    packages = find_installed_packages(package_specifier)
    if packages:
        catalogue = read_catalogue()
        for package in packages:
            uninstaller(package)
            catalogue[package.project.id].remove(package)
        write_catalogue(catalogue)
    else:
        return error("Not installed.")


def dump_package(package):
    return (package.project.id, package.attributes)

def load_package(blob):
    return package.Package(recipe.get_project(blob[0]), blob[1])

def find_installed_packages(package_specifier):
    r = []
    catalogue = read_catalogue()
    for package in catalogue[package_specifier.project]:
        if package_specifier.match(package):
            r.append(package)
    return r

def get_packages():
    r = []
    catalogue = read_catalogue()
    for project, packages in catalogue.items():
        r.extend(packages)
    return r



def read_catalogue():
    r = defaultdict(list)
    if exists(catalogue_path):
        with open(catalogue_path, 'rb') as catalogue_file:
            for blob in pickle.load(catalogue_file):
                package = load_package(blob)
                r[package.project.id].append(package)
    return r


def write_catalogue(catalogue):
    blobs = []
    for packages in catalogue.values():
        blobs.extend(map(dump_package, packages))
    with open(catalogue_path, 'wb') as catalogue_file:
        pickle.dump(blobs, catalogue_file)


repository.register('standard', 'Standard', get_packages)
