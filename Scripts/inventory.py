from collections import defaultdict
import sys

import colorama

from command import command

import repository
import select


reset_style = colorama.Fore.RESET + colorama.Back.RESET + \
              colorama.Style.RESET_ALL


@command()
def inventory(args):
    """List installed packages.

    Options:
        -m   Print project IDs and attributes. 
    """

    if '-m' in args:
        print_machine_inventory()
    elif '-w' in args:
        print_wide_inventory()
    else:
        print_tabular_inventory(args)


def print_machine_inventory():
    for package in repository.get_packages():
        print package


def style(package, is_selected):
    if is_selected:
        return ''
    return colorama.Fore.BLUE


def print_wide_inventory():
    selected = set(select.get_selected_packages())

    packages = repository.get_packages()
    packages.sort(key=lambda p: (p.project.namespace, p.project.id))

    format = lambda p: p.project.qualified_id

    cells = [
        style(p, p in selected) + format(p) + reset_style
        for p in packages
    ]

    cells = []
    for p in packages:
        text = format(p)
        cells.append((p, text))

    width = max(map(len, map(format, packages)))
    cols = 79 // width

    for row in chop(cells, cols):
        for (package, text) in row:
            print style(package, package in selected),
            print text.ljust(width),
            print reset_style,
        print ''


def chop(xs, n):
    "chop([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]"
    ys = []
    for x in xs:
        ys.append(x)
        if len(ys) == n:
            yield ys
            ys = []
    if ys:
        yield ys


def print_tabular_inventory(args):

    selected = set(select.get_selected_packages())

    packages = repository.get_packages()
    packages.sort(key=lambda p: p.project.name)


    columns = [
        lambda p: p.project.qualified_id,
        lambda p: p.project.name,
        lambda p: p.attributes.get('version', ''),
    ]

    rows = []

    for i, package in enumerate(packages):
        row = []
        for column in columns:
            cell = column(package)
            width = len(cell)
            if width > getattr(column, 'width', 0):
                column.width = width
            row.append(cell)
        rows.append((row, package))

    for row, package in rows:
        print style(package, package in selected), '',
        for i, column in enumerate(columns):
            if i == 0:
                print row[i].rjust(column.width),
            else:
                print row[i].ljust(column.width),

        print reset_style

