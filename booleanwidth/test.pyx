cdef extern from "uint128.h":
    ctypedef unsigned long long uint128

from .profiling import profile

#cdef extern from "bitsetfoo.h":
    #cdef cppclass BitSet128:
        #int value
        #BitSet128()
        #BitSet128 fromint(int)
        #BitSet128 operator+(BitSet128)
        #BitSet128 operator-(BitSet128)
        #BitSet128 operator&(BitSet128)
        #BitSet128 operator|(BitSet128)
cdef class BitSet128:
    cdef public long value

    def __init__(self, value):
        self.value = value

    #BitSet128 operator+(BitSet128)
    #BitSet128 operator-(BitSet128)
    #BitSet128 operator&(BitSet128)
    #BitSet128 operator|(BitSet128)
    def __add__(self, other):
        return BitSet128(self.value + other.value)

    def __mul__(self, other):
        return BitSet128(self.value * other.value)

    def __and__(self, other):
        return BitSet128(self.value & other.value)

    def __or__(self, other):
        return BitSet128(self.value | other.value)

    def __xor__(self, other):
        return BitSet128(self.value ^ other.value)

    def __richcmp__(self, comp, other):
        print(self)
        print(comp)
        print(other)
        if comp == 0:
            return self.value < other.value
        if comp == 1:
            return self.value <= other.value
        if comp == 2:
            return self.value == other.value
        if comp == 3:
            return self.value != other.value
        if comp == 4:
            return self.value > other.value
        if comp == 5:
            return self.value >= other.value

    def __contains__(self, other):
        return self | other == self

    #def __len__(self):
        #return size(self.other)

    # TODO: replace with __next__
    #def __iter__(self):
        #return iterate(self.other)

    def __str__(self):
        return 'BitSet128({})'.format(self.value)

cpdef f():
    cdef long long a = 1
    cdef long long b = 1
    cdef long long c = 1
    #cdef long long d = 1
    #a = BitSet128(1)
    #b = BitSet128(1)
    #c = BitSet128(1)
    #d = BitSet128(1)
    #bound = BitSet128(100000000)
    #while a < bound:
    for _ in range(1000000):
        a = a + (a & b) | c
        #d = BitSet128(1)
        #while d < bound:
            #d += (a & b) | c
    return a

def test():
    profile(f)
