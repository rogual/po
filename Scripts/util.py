import subprocess
import struct
import stat
import sys
import os

def require_register_width(x):
    rw = 8 * struct.calcsize('P')
    if rw != x:
        raise Exception(
            "%-bit Python not supported. Please use %s-bit Python." % (rw, x))

def error(message):
    print >>sys.stderr, message
    return 1

def rmtree(top):
    """Like shutil.rmtree but doesn't fail on read-only files."""
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

def run(cmd, *a, **kw):
    print cmd
    ret = subprocess.call(cmd, *a, **kw)
    if ret:
        raise Exception("External command failed with status %s" % ret)
