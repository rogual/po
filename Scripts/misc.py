import package
import repository
import environment
import attributes
import paths

from util import error


@package.command()
def cd(package_specifier):
    """Change to the directory of the specified package.

    If called without arguments, change to the Site directory.
    """

    if package_specifier:
        path, err = get_path(package_specifier)
        if err:
            return err
    else:
        path = paths.site

    with environment.exit() as exit:
        exit.write('@cd "%s"\n' % path)


@package.command()
def which(package_specifier):
    """Show where the specified package is installed."""

    if package_specifier:
        path, err = get_path(package_specifier)
        if err:
            return err
    else:
        return error("Usage: po which PACKAGE")


def get_path(package_specifier):
    ps = list(repository.find_installed_packages(package_specifier))

    if len(ps) == 0:
        return error("No matching packages."), None
    elif len(ps) != 1:
        return error("Ambiguous command."), None

    path = ps[0].get(attributes.a_location)
    if not path:
        return error("Package has no associated location."), None

    return None, path
