"""The Standard repository holds 3rd party projects."""

from util import error
from os.path import join, exists
from os import makedirs
from collections import defaultdict

import repository
import attributes
import catalogue
import download
import package
import project
import select
import recipe
import paths
import util


catalogue_path = join(paths.state, 'catalogue')

no_factory = {}

# Projects can implement these
factory = project.interface(lambda prj, spec: no_factory)
installer = project.interface()
uninstaller = project.interface()


# These attributes are now common
a_location = attributes.a_location


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
    with catalogue.modify(catalogue_path) as cat:
        cat[package.project.id].append(package)

    # If no packages from this project are already selected, select this one.
    selected = select.get_selected_packages()
    if not any(p for p in selected if p.project.id == project_id):
        select.select_package(package)


@package.command()
def uninstall(package_specifier):
    """Uninstall a package."""
    packages = find_installed_packages(package_specifier)
    if packages:
        cat = catalogue.read(catalogue_path)
        for package in packages:
            select.deselect_package(package)
            uninstaller(package)
            cat[package.project.id].remove(package)
        catalogue.write(catalogue_path, cat)
    else:
        return error("Not installed.")


def find_installed_packages(package_specifier):
    r = []
    cat = catalogue.read(catalogue_path)
    for package in cat[package_specifier.project]:
        if package_specifier.match(package):
            r.append(package)
    return r


def get_packages():
    r = []
    cat = catalogue.read(catalogue_path)
    for project, packages in cat.items():
        r.extend(packages)
    return r

repository.register(
    'standard', 'Standard', get_packages, find_installed_packages
)
