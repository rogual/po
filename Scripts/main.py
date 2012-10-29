import sys

import command

# These register things
import environment
import repository
import standard
import system
import local

if __name__ == '__main__':
    sys.exit(command.run(sys.argv[1:]))

