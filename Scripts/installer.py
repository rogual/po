from os.path import expanduser, join, exists, abspath
import os
import sys
import json
import zipfile
import urllib2
import StringIO

url = 'http://github.com/robin-allen/po/archive/master.zip'

home = expanduser('~')

load_script = '''
@doskey po="{python}" ^
  "{path}\Scripts\main.py" $* ^& ^
  "{path}\State\exit.bat"
'''[1:]

success = '''
Installation complete. To make the po command available, run the batch file
located at:

{path}

You might want to change your command prompt settings to run this file at
startup.
'''


def ask(question, default):
    print question
    print "Default:", default
    r = None
    while not r:
        r = abspath(expanduser(raw_input('?! ') or default))
        #if exists(r):
            #print 'Directory exists; please choose another.'
            #r = None
    return r


def install():
    packages_path = ask("Packages path?", join(home, 'Packages'))
    site_path = ask("Site path?", join(home, 'Site'))

    print "Confirm settings:"
    print "  Packages:", packages_path
    print "      Site:", site_path

    print

    raw_input("Ctrl-C to quit, any other input to install: ")

    pm_path = join(packages_path, 'Package Manager')

    print 'Downloading.'
    download(pm_path)

    print 'Installing.'
    state_path = join(pm_path, 'State')
    cache_path = join(pm_path, 'Cache')

    for path in state_path, cache_path:
        if not exists(path):
            os.makedirs(path)

    open(join(state_path, 'exit.bat'), 'w').close()

    settings_path = join(state_path, 'settings.json')
    load_path = join(state_path, 'load.bat')

    with open(load_path, 'wt') as loader:
        loader.write(load_script.format(
            python=sys.executable,
            path=pm_path
        ))

    with open(settings_path, 'wt') as settings:
        settings.write(json.dumps({
            'packages': packages_path,
            'site': site_path
        }))

    print success.format(path=load_path)


def download(dest):
    try:
        request = urllib2.urlopen(get_url())
        data = request.read()
        archive = zipfile.ZipFile(StringIO.StringIO(data))
        extract_with_prefix(archive, dest, 'po-master')
    except urllib2.HTTPError as e:
        print 'There was a network error:'
        print str(e)
        sys.exit(1)


def extract_with_prefix(archive, dest, prefix):
    """Extract an archive, stripping prefix from paths where present."""
    def members():
        for info in archive.infolist():
            name = info.filename
            if name.startswith(prefix):
                name = name[len(prefix):]
                while name and name[0] in '\\/':
                    name = name[1:]
            if name:
                info.filename = name
                yield info
    archive.extractall(dest, members=members())


def get_url():
    if len(sys.argv) == 2:
        return sys.argv[1]
    return url


if __name__ == '__main__':
    try:
        install()
    except KeyboardInterrupt:
        print '\nCancelled.'
        pass
