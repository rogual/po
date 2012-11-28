from os.path import join, normpath
import os
import contextlib

from command import command

import attributes
import package
import project
import paths
import select
import util

exit_path = join(paths.state, 'exit.bat')

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


def define_paths(project, paths):
    """Helper function to define paths for a project."""
    if isinstance(paths, dict):
        paths = paths.items()

    def loc(pkg):
        return pkg[attributes.a_location]

    for k, v in paths:
        def doit(k, v):

            if isinstance(v, basestring):
                v = [v]

            def get(pkg):
                def to_path(x):
                    return normpath(join(loc(pkg), x))
                return map(to_path, v)

            k.implement(project)(get)

        doit(k, v)



@command()
def cmd_paths(args):
    """Query environment variables."""
    print os.environ[args or 'PATH'].replace(';', '\n')


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


@contextlib.contextmanager
def exit():
    with open(exit_path, 'wt') as exit:
        yield exit
        # Have exit.bat blank itself after use
        exit.write("@type nul > \"%~f0\"\n")

def reload():
    # The po wrapper script executes exit.bat after every command, so we can
    # write to it to modify the calling environment.
    if 'PO_SUBSHELL' in os.environ:
        with exit() as f:
            write_batch_file(f)

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
