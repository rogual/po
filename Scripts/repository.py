from command import command

repositories = []

class Repository:
    def get_packages(self):
        pass


@command()
def inventory(args):
    """List installed packages.

    Options:
        -m   Print project IDs and attributes. 
    """
    if '-m' in args:
        for package in get_packages():
            print package
    else:
        for package in get_packages():
            print package.project.name


def register(id, name, get_packages):
    """Create and register a repository."""
    repo = Repository()
    repo.id = id
    repo.name = name
    repo.get_packages = get_packages
    repositories.append(repo)


def get_packages():
    """Return a list of all packages in all repositories."""
    packages = []
    for repo in repositories:
        packages.extend(repo.get_packages())
    return packages


def get_list(interface):
    result = []
    for package in get_packages():
        result.extend(interface(package))
    return result


