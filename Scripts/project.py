from collections import defaultdict

import package


class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def nop(*a, **kw):
    pass


def interface(default=nop):
    """Generic function dispatching on its first argument, which can be a
    package or project. Can be implemented for each project."""
    def call(target, *a, **kw):
        if isinstance(target, package.Package):
            project = target.project
        else:
            project = target
        impl = call.impl.get(project, default)
        return impl(target, *a, **kw)
    call.impl = {}

    def implement(project):
        def deco(fn):
            call.impl[project] = fn
            return fn
        return deco
    call.implement = implement

    return call


