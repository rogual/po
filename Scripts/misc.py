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
        ps = list(repository.find_installed_packages(package_specifier))

        if len(ps) == 0:
            return error("No matching packages.")
        elif len(ps) != 1:
            return error("Ambiguous command.")

        path = ps[0].get(attributes.a_location)
        if not path:
            return error("Package has no associated location.")
    else:
        path = paths.site

    with environment.exit() as exit:
        exit.write('@cd "%s"\n' % path)

