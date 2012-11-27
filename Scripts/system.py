import repository
import project
import recipe

scan = project.interface(lambda pkg: [])


def get_packages():
    return recipe.get_list(scan)


def find_installed_packages(package_specifier):
    r = []
    for package in get_packages():
        if package_specifier.match(package):
            r.append(package)
    return r


repository.register('system', 'System', get_packages, find_installed_packages)
