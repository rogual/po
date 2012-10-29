import project
import package
import system
import environment
import paths

recipe = project.Project('po', "Package Manager")

@system.scan.implement(recipe)
def scan(project):
    return [package.Package(project)]

@environment.executables.implement(recipe)
def bin(recipe):
    return [paths.executables]
