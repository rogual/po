from os.path import expanduser, join, exists, abspath
import sys
import json

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
    print 'Installing.'

    pm_path = join(packages_path, 'Package Manager')
    state_path = join(pm_path, 'State')
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

if __name__ == '__main__':
    try:
        install()
    except KeyboardInterrupt:
        print '\nCancelled.'
        pass
