# Enable importing Cython modules
import pyximport
pyximport.install()

import cProfile

from graph64 import to64
from bitset64 import subsets, tostring

