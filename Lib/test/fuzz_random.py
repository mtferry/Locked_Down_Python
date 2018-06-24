# Fuzz Tests for _random

import test.fuzzhelper as fh
import _random

# from _randommodule.c, line 76
N = 624

def fh_tuple():
  return tuple(fh.int() for _ in range(N+1))

def test():
  for _ in range(9999):
    fh.check(_random,
             valid_inputs = [
                            ((),{}),
                            ((fh.object,),{}),
                            ((fh_tuple,),{}),
                            ],
             expected_exceptions = (TypeError))

if __name__ == '__main__': fh.do_test_loop(test)
