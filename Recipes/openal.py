from os.path import join

import project
import package
import environment
import system

from attributes import a_location

recipe = project.Project('openal', "OpenAL")

path = r'C:\Program Files (x86)\OpenAL 1.1 SDK'


@system.scan.implement(recipe)
def scan(project):
    return [
        package.Package(project, {
            a_location: path
        })
    ]


environment.define_paths(recipe, {
    environment.libraries: ['libs\\Win32'],
    environment.headers: ['include'],
    environment.executables: ['bin']
})
