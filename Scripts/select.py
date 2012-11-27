from os.path import join

import environment
import repository
import catalogue
import standard
import package
import system
import local
import paths
import util


segment_path = join(paths.state, 'segment')


@package.command()
def select(package_specifier):
    """Select a package.

    Only selected packages are considered when building up the environment
    for 'po enter'.
    """

    to_select = repository.find_installed_packages(package_specifier)
    if not to_select:
        return util.error("No matching packages.")

    project_specifier = package.Specifier(package_specifier.project, {})
    to_deselect = repository.find_installed_packages(project_specifier)

    map(deselect_package, to_deselect)
    map(select_package, to_select)


@package.command()
def deselect(package_specifier):
    "Deselect a package."
    map(deselect_package, repository.find_installed_packages(package_specifier))


def get_selected_packages():
    installed = set(repository.get_packages())
    segment = catalogue.read(segment_path)
    for project_id, packages in segment.items():
        for package in packages:
            if package in installed:
                yield package


def select_package(package):
    with catalogue.modify(segment_path) as segment:
        segment[package.project.id].append(package)
    environment.reload()


def deselect_package(package):
    with catalogue.modify(segment_path) as segment:
        remove_all(segment[package.project.id], package)
    environment.reload()


def remove_all(xs, y):
    xs[:] = [x for x in xs if x != y]
