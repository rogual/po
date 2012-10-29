from os.path import join
import simple
import standard

url = "http://downloads.sourceforge.net/project/" \
      "unxutils/unxutils/current/UnxUtils.zip"

# Windows requres admin privileges to run any file with "patch" in its name
# unless it has a manifest like this.
manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
<security>
<requestedPrivileges>
<requestedExecutionLevel level="asInvoker" uiAccess="false"/>
</requestedPrivileges>
</security>
</trustInfo>
</assembly>
"""

recipe = simple.simple('unixutils', 'Unix Utilities', url)

@standard.installer.implement(recipe)
def do_install(package):
    path = simple.download_and_extract(url, package)
    mpath = join(path, 'usr', 'local', 'wbin', 'patch.exe.manifest')
    with open(mpath, 'wt') as file:
        file.write(manifest)
