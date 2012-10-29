import simple
import standard
import environment

url = "http://the.earth.li/~sgtatham/putty/latest/x86/putty.zip"

recipe = simple.simple('putty', 'PuTTY', url)

@environment.executables.implement(recipe)
def bin(package):
    return [package[standard.a_location]]
