from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

# extensions = [
#Extension("main", 'main.pyx'),
#Extension("bitset", 'bitset.pyx')
#]

setup(
    ext_modules=cythonize(
        '*.pyx',
        include_dirs='.',
        compiler_directives={'profile': True}
    )
)
