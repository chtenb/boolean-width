from .bitset128 import iterate, uint128
from .bitset import BitSet as BitSet

def run():
    x = BitSet()
    counter = 10000

    while counter:
        counter -= 1
        for v in BitSet(2 ** 50 - 1):
            x |= v

    print(x)

def runcint():
    cdef uint128 v = 0, x = 0
    cdef int counter = 10000

    while counter:
        counter -= 1
        for v in iterate(2 ** 50 - 1):
            x |= v

    print(x)


