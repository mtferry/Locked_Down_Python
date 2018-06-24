# Fuzz Tests for _csv

import test.fuzzhelper as fh
import _csv

def test():
  for _ in range(9999):
    fh.check(_csv,
             valid_inputs = [
                            ((),{}),
                            ((fh.int,),{}),                           
                            ((fh.bytes,),{}),                           
                            ((fh.bytes, fh.dict),{}),                           
                            ((fh.list,),{}),                           
                            ((fh.list, fh,bytes),{}),                           
                            ((fh.list, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes),{}),                           
                            ((fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes),{}),                           
                            ((fh.bytes, fh.dict, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes, fh.bytes),{}),                           
                            ],
             expected_exceptions = (TypeError, ValueError, _csv.Error))

if __name__ == '__main__': fh.do_test_loop(test)
