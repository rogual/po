from os.path import join
import os

from command import command

import package
import project
import paths
import select
import util


executables = project.interface(lambda pkg: [])
initializers = project.interface(lambda pkg: [])
headers = project.interface(lambda pkg: [])
libraries = project.interface(lambda pkg: [])
pythonpath = project.interface(lambda pkg: [])

interface_vars = [
    (executables, 'PATH'),
    (headers, 'INCLUDE'),
    (libraries, 'LIB'),
    (pythonpath, 'PYTHONPATH')
]


@command()
def enter(args):
    """Enter the environment.
    
    Starts a new sub-shell with environment variables provided by selected
    packages.

    While in the sub-shell, the shell prompt will start with [P]. Commands
    from installed packages will be available.
    """

    if 'PO_SUBSHELL' in os.environ:
        return util.error("Already in a po environment.")

    init_path = join(paths.state, 'init.bat')
    with open(init_path, 'wt') as init:
        write_batch_file(init)

    try:
        os.system('cmd /k "%s"' % init_path)
    except KeyboardInterrupt:
        pass


@command()
def load(args):
    """Reload the environment.
    
    Populate the current environment with variables provided by selected
    packages.
    
    Like 'enter', but operates on the calling environment rather than starting
    a subshell."""
    reload()


def reload():
    # The po wrapper script executes exit.bat after every command, so we can
    # write to it to modify the calling environment.
    if 'PO_SUBSHELL' in os.environ:
        exit_path = join(paths.state, 'exit.bat')
        with open(exit_path, 'wt') as exit:
            write_batch_file(exit)
            
            # Have exit.bat blank itself after use
            exit.write("type nul > \"%~f0\"\n")


def get_list(interface):
    result = []
    for package in select.get_selected_packages():
        result.extend(interface(package))
    return result


def write_batch_file(batch):
    batch.write('@echo off\n')
    batch.write('prompt [P] $P$G\n')
    batch.write('SET PO_SUBSHELL=1\n')

    for interface, var in interface_vars:
        base = 'PO_BASE_' + var

        vars = {'base': base, 'var': var}
        batch.write('IF "%{base}%"=="" SET {base}=%{var}%\n'.format(**vars))
        batch.write('SET {var}=%{base}%\n'.format(**vars))

        for path in get_list(interface):
            vars['path'] = path
            batch.write('SET {var}={path};%{var}%\n'.format(**vars))

    for cmd in get_list(initializers):
        if isinstance(cmd, basestring):
            cmd = [cmd]

        batch.write(' '.join(['call'] + map(quote, cmd)))
        batch.write('\n')


def quote(x):
    return '"%s"' % x.replace('"', '^"')
