import util
import textwrap
import sys
import re

commands = {}

def command(name=None):
    """Decorator for defining commands"""
    def deco(fn):
        fn.name = name or fn.__name__
        if fn.name.startswith('cmd_'):
            fn.name = fn.name[4:]
        commands[fn.name] = fn
        return fn
    return deco


def run(argv):
    """Parse a command line and run the appropriate command. Return 0 on
    success, -1 if a command could not be found, or a nonzero number on
    error."""
    if not argv:
        help()
        return -1

    head, tail = argv[0], ' '.join(argv[1:])

    command = lookup_command(head)

    return command(tail) or 0


def summarize(command):
    """Return a short blurb describing the command."""
    if command.__doc__:
        return command.__doc__.split('.', 1)[0].strip()
    return ''


@command()
def help(name=None):
    """Show available commands"""
    if name:
        command = lookup_command(name)
        print command.__doc__ or "Undocumented command."
        return

    print "Usage: po COMMAND [ARGS]"
    print
    print "Available commands:"
    spacing = 16
    hang = spacing + 2
    wrap = textwrap.TextWrapper(
        initial_indent='',
        subsequent_indent=' ' * hang
    )
    for name in sorted(commands.keys()):
        summary = re.sub(' +', ' ', summarize(commands[name]))
        print '  ' + name.ljust(spacing) + wrap.fill(summary)
    print
    print "To get help on a command:"
    print "  po help COMMAND"


def lookup_command(head):
    """Prefix search on commands. Prints message on error."""
    candidates = filter(lambda x: x.startswith(head), commands.keys())
    if len(candidates) == 0:
        help()
        sys.exit(-1)
    elif len(candidates) == 1:
        return commands.get(candidates[0])
    else:
        sys.exit(util.error(
            "Ambiguous command. Could be:\n" +
            '\n'.join('  ' + c for c in candidates)
        ))


