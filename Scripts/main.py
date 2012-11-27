import os
import sys

sys.path.append(os.path.dirname(__file__) + '/../Libraries')

import colorama
colorama.init()

import command

# These register things
import environment
import repository
import inventory
import standard
import system
import select
import local

if __name__ == '__main__':
    sys.exit(command.run(sys.argv[1:]))

