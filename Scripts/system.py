import repository
import project
import recipe

scan = project.interface(lambda pkg: [])


def get_packages():
    return recipe.get_list(scan)

repository.register('system', 'System', get_packages)
