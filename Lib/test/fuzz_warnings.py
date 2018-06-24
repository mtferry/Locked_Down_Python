# Fuzz Tests for _warnings

import test.fuzzhelper as fh
import _warnings

def test():
  for _ in range(9999):
    fh.check(_warnings,
             valid_inputs = [
                            ((),{}),
                            ((fh.bytes, fh.object, fh.int, fh.bytes),{}),
                            ((fh.bytes, fh.object, fh.bytes, fh.int, fh.bytes, fh.object, fh.object, fh.object),{})
                            ],
             expected_exceptions = (TypeError))

if __name__ == '__main__':
  fh.do_test_loop(test)
else:
  import warnings
  warnings.filterwarnings('ignore')
