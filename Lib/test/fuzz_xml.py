# Fuzz Tests for pyexpat

import test.fuzzhelper as fh
import pyexpat

def test():
  for _ in range(9999):
    fh.check(pyexpat,
             valid_inputs = [
                             ((),{}),
                             ((fh.bool,),{}),
                             ((fh.int,),{}),
                             ((fh.str,),{}),
                             ((fh.bytes,),{}),
                             ((fh.str, fh.bool),{}),
                             ((fh.str, fh.str),{}),
                             ((fh.bytes, fh.bool),{}),
                             ((fh.file_object,),{}),
                             ((fh.str, fh.str, fh.dict),{})
                            ],
             expected_exceptions = (TypeError, ValueError))

if __name__ == '__main__': fh.do_test_loop(test)
