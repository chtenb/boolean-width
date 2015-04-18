#from distutils.core import setup
#from Cython.Build import cythonize
#from distutils.extension import Extension

# extensions = [
#Extension("main", 'main.pyx'),
#Extension("bitset", 'bitset.pyx')
#]

# setup(
# ext_modules=cythonize(
#'*.pyx',
# include_dirs='.',
#compiler_directives={'profile': True}
#)
#)

# build script for 'dvedit' - Python libdv wrapper

# change this as needed
#libdvIncludeDir = "/usr/include/libdv"

import sys
import os
from distutils.core import setup
from distutils.extension import Extension

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except ImportError:
    print("""You don't seem to have Cython installed. Please get a copy from www.cython.org and
            install it""")
    sys.exit(1)


# scan the 'dvedit' directory for extension files, converting
# them to extension names in dotted notation
def scandir(directory, files=None):
    if files == None:
        files = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


# generate an Extension object from its dotted name
def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep) + ".pyx"
    return Extension(
        extName,
        [extPath],
        # include_dirs = [libdvIncludeDir, "."],   # adding the '.' to
        # include_dirs is CRUCIAL!!
        include_dirs=["."],   # adding the '.' to include_dirs is CRUCIAL!!
        #extra_compile_args = ["-O3", "-Wall"],
        extra_compile_args=[],
        #extra_link_args = ['-g'],
        extra_link_args=[],
        #libraries = ["dv",],
        libraries=[]
    )

# get the list of extensions
extNames = scandir("booleanwidth")

# and build up the set of Extension objects
extensions = [makeExtension(name) for name in extNames]

# finally, we can pass all this to distutils
setup(
    name="booleanwidth",
    packages=["booleanwidth", "booleanwidth.experiments"],
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext},
    compiler_directives={'profile': True}
)
