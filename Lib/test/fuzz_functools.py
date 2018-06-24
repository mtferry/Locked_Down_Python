# Fuzz Tests for _functools

import test.fuzzhelper as fh
import _functools

def test():
  for _ in range(9999):
    fh.check(_functools,
             valid_inputs = [
                            ((),{}),
                            ((fh.tuple,),{}),
                            ((fh.function),{}),
                            ((fh.function, fh.list, fh.object),{}),
                            ((fh.int, fh.bool),{}),
                            ],
             expected_exceptions = (TypeError))

if __name__ == '__main__': fh.do_test_loop(test)
