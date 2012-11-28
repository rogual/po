from collections import namedtuple

from command import command as normal_command

import repository

class Package:
    def __init__(self, project, attributes=None):
        self.project = project
        self.attributes = attributes or {}
        self.__getitem__ = self.attributes.__getitem__
        self.__contains__ = self.attributes.__contains__
        self.get = self.attributes.get
        for key in self.attributes.keys():
            assert valid_attribute(key)

    def __hash__(self):
        return sum(map(
            hash,
            [self.project.id] + list(self.attributes.items())
        ))

    def __setitem__(self, key, value):
        assert valid_attribute(key)
        self.attributes[key] = value

    def __eq__(self, other):
        if self.project.id != other.project.id:
            return False
        if self.attributes != other.attributes:
            return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return '%s (%s)' % (
            self.project.id,
            ', '.join(
                '%s=%s' % (k, repr(v)) for k, v in self.attributes.items()
            )
        )

    def __repr__(self):
        return 'Package(%s, %s)' % (
            repr(self.project),
            repr(self.attributes))

    def replace(args):
        attrs = self.attributes.copy()
        attrs.update(args)
        return Package(self.project, attrs)


attributes = {}

def attribute(id, name):
    assert id not in attributes
    attributes[id] = name
    return id

def valid_attribute(id):
    return id in attributes


class Specifier:
    def __init__(self, project, arguments):
        self.project = project
        self.arguments = arguments
        self.get = self.arguments.get

    def __nonzero__(self):
        return 1 if self.project or self.arguments else 0

    def match(self, package):
        if self.project != package.project.id:
            return False

        for k, v in self.arguments.items():
            if package.attributes.get(k) != v:
                return False

        return True

    def __repr__(self):
        return 'Specifier(%s, %s)' % (
            repr(self.project),
            repr(self.arguments)
        )


def command(name=None):
    """Decorator for defining commands which take package specifiers. Parses
    the specifier and calls the decorated function with it."""
    def deco(fn):
        def wrap(specifier):
            return fn(parse_specifier(specifier))
        wrap.__name__ = fn.__name__
        wrap.__doc__ = fn.__doc__
        return normal_command(name)(wrap)
    return deco


def parse_specifier(specifier_string):
    arguments = {}
    bits = specifier_string.split(' ')
    project_specifier = bits[0]
    for bit in bits[1:]:
        arg, val = bit.split('=', 1)
        arguments[arg] = val

    return Specifier(project_specifier, arguments)

