# Fuzz Tests for _tracemalloc

import test.fuzzhelper as fh
import _tracemalloc

def test():
  for _ in range(9999):
    fh.check(_tracemalloc,
             valid_inputs = [
                            ((),{}),
                            ((fh.object,),{}),                           
                            ],
             expected_exceptions = (TypeError, ValueError))

if __name__ == '__main__': fh.do_test_loop(test)
