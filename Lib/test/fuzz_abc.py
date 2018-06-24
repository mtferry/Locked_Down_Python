# Fuzz Tests for _abc

import test.fuzzhelper as fh
import _abc

def test():
  for _ in range(9999):
    fh.check(_abc,
             valid_inputs = [
                            ((),{}),
                            ((fh.klass,),{}),
                            ((fh.klass,fh.klass),{}),
                            ],
             expected_exceptions = (TypeError, AttributeError))

if __name__ == '__main__': fh.do_test_loop(test)
