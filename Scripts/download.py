from os.path import commonprefix

import urllib2
import zipfile
import tarfile


def url_filename(url):
    if '?' in url:
        url = url.split('?', 1)[0]
    return url.rsplit('/', 1)[-1]


def download(url, path):
    """Downloads the resource at the given URL to the given path."""
    request = urllib2.urlopen(url)
    out = open(path, 'wb')
    meta = request.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = request.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        out.write(buffer)
        status = r"Downloading [%3.2f%%]" % (
            file_size_dl * 100. / file_size
        )
        status = status + chr(8)*(len(status)+1)
        print status,
    print

    out.close()
    return path


def extract(path, dest, prefix=None):
    """Extracts the archive at path to a new folder at dest, which should not
    already exist."""
    if path.endswith('.zip'):
        archive = zipfile.ZipFile(path)
        use_prefix = prefix or commonprefix(archive.namelist())
        if use_prefix:
            extract_with_prefix(archive, dest, use_prefix)
        else:
            archive.extractall(dest)
    else:
        archive = tarfile.open(path)

        use_prefix = prefix or commonprefix(archive.getnames())
        if use_prefix:
            extract_with_prefix(archive, dest, use_prefix)
        else:
            archive.extractall(dest)


def extract_with_prefix(archive, dest, prefix):
    """Extract an archive, stripping prefix from paths where present."""
    def members():
        for info in iterate_info(archive):
            name = get_info_name(info)
            if name.startswith(prefix):
                name = name[len(prefix):]
                if name:
                    while name[0] in '\\/':
                        name = name[1:]
            if name:
                set_info_name(info, name)
                yield info
    archive.extractall(dest, members=members())


# Account for inconsistencies in Python stdlib

def iterate_info(archive):
    """Yields each info member of a tar or zip archive"""
    if isinstance(archive, zipfile.ZipFile):
        for info in archive.infolist():
            yield info
    else:
        for info in archive:
            yield info


def get_info_name(info):
    return getattr(info, info_name_attr(info))


def set_info_name(info, name):
    setattr(info, info_name_attr(info), name)


def info_name_attr(info):
    if isinstance(info, zipfile.ZipInfo):
        return 'filename'
    else:
        return 'name'

