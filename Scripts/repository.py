
repositories = []

class Repository:
    def get_packages(self):
        pass


def register(id, name, get_packages, find_installed_packages):
    """Create and register a repository."""
    repo = Repository()
    repo.id = id
    repo.name = name
    repo.get_packages = get_packages
    repo.find_installed_packages = find_installed_packages
    repositories.append(repo)


def get_packages():
    """Return a list of all packages in all repositories."""
    packages = []
    for repo in repositories:
        packages.extend(repo.get_packages())
    return packages


def get_packages_with_repos():
    packages = []
    for repo in repositories:
        for package in repo.get_packages():
            packages.append((repo, package))
    return packages


def find_installed_packages(specifier):
    for repo in repositories:
        for package in repo.find_installed_packages(specifier):
            yield package




