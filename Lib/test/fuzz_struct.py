# Fuzz Tests for _struct, _heapq, _bisect and _collections

import test.fuzzhelper as fh
import _struct, _heapq, _bisect, _collections

def test():
  for _ in range(999):
    common_exceptions = (TypeError, ValueError, AttributeError, IndexError, ImportError)

    fh.check(_struct,
             valid_inputs = [
                            ((fh.str,),{}),
                            ((fh.bytes,),{}),
                            ((fh.str, fh.bytes, fh.int),{}),
                            ((fh.str, fh.bytes, fh.int, fh.int),{}),
                            ((fh.str, fh.int),{}),
                            ((fh.str, fh.bytes),{}),
                            ],
             expected_exceptions = common_exceptions + (LookupError, _struct.error))

    fh.check(_heapq,
             valid_inputs = [
                            ((),{}),
                            ((fh.list,),{}),
                            ((fh.list, fh.object),{})
                            ],
             expected_exceptions = common_exceptions)
    
    fh.check(_bisect,
             valid_inputs = [((fh.list,fh.object,fh.int,fh.int),{})],
             expected_exceptions = common_exceptions)

    fh.check(_collections,
             valid_inputs = [
                            ((fh.list,),{}),
                            ((fh.list, fh.int),{}),
                            ((fh.object,),{}),
                            ((fh.object, fh.int),{}),
                            ((fh.object, fh.int, fh.int),{})
                            ],
             expected_exceptions = common_exceptions + (LookupError,))

if __name__ == '__main__': fh.do_test_loop(test)
