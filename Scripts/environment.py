from os.path import join
import os

from command import command

import package
import project
import repository
import paths


executables = project.interface(lambda pkg: [])
initializers = project.interface(lambda pkg: [])
headers = project.interface(lambda pkg: [])
libraries = project.interface(lambda pkg: [])
pythonpath = project.interface(lambda pkg: [])


@command()
def enter(args):
    """Enter the environment.
    
    Starts a new sub-shell with environment variables provided by installed
    packages.

    While in the sub-shell, the shell prompt will start with [P]. Commands
    from installed packages will be available, as well as the following
    commands:

        exit -- Exit the sub-shell
        init -- Reload environment variables
    """
    init_path = join(paths.state, 'init.bat')
    with open(init_path, 'wt') as init:
        init.write('@echo off\n')
        init.write('prompt [P] $P$G\n')

        for interface, var in (
            (executables, 'PATH'),
            (headers, 'INCLUDE'),
            (libraries, 'LIB'),
            (pythonpath, 'PYTHONPATH')
        ):
            base = 'PO_BASE_' + var

            vars = {'base': base, 'var': var}
            init.write('IF "%{base}%"=="" SET {base}=%{var}%\n'.format(**vars))
            init.write('SET {var}=%{base}%\n'.format(**vars))

            for path in repository.get_list(interface):
                vars['path'] = path
                init.write('SET {var}={path};%{var}%\n'.format(**vars))

        for cmd in repository.get_list(initializers):
            init.write('"%s"\n' % cmd)

        init.write("SET PATH=" + paths.state + ";%PATH%\n")

    os.system('cmd /k "%s"' % init_path)
