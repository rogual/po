from os.path import join

import simple
import environment
import standard

url = "https://chromiumembedded.googlecode.com/" \
      "files/cef_binary_1.1180.832_windows.zip"

recipe = simple.simple('cef', 'Chromium Embedded Framework', url)


@environment.libraries.implement(recipe)
def libraries(package):
    loc = package[standard.a_location]
    return [join(loc, 'lib', 'Release'), join(loc, 'Release', 'lib')]


@environment.headers.implement(recipe)
def include(package):
    loc = package[standard.a_location]
    return [loc, join(loc, 'include')]
