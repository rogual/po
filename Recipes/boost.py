import simple
import environment
import standard

url = "http://downloads.sourceforge.net/project/" \
      "boost/boost/1.51.0/boost_1_51_0.tar.bz2"

recipe = simple.simple(
    'boost', "Boost C++ Libraries", url, prefix='./boost_1_51_0'
)

@environment.headers.implement(recipe)
def find_headers(package):
    return [package[standard.a_location]]
