# Fuzz Tests for _io

import test.fuzzhelper as fh
import _io

def dir_func(i):
  d = set(dir(i))
  if '_CHUNK_SIZE' in d:
    try: setattr(i, '_CHUNK_SIZE', fh.object())
    except ValueError: pass
  return d - set(['FileIO', '_WindowsConsoleIO', 'open'])
  
def test():
  for _ in range(9999):
    fh.check(_io,
             valid_inputs = [
                            ((),{}),
                            ((fh.int,),{}),
                            ((fh.bytes,),{}),
                            ((_io.BytesIO, fh.int),{}),
                            ((_io.BytesIO, _io.BytesIO, fh.int),{}),
                            ((_io.BytesIO, _io.BytesIO, fh.int),{}),
                            ((_io.BytesIO, fh.int, fh.int),{}),
                            ((fh.tuple),{}),
                            ],
             expected_exceptions = (TypeError, AttributeError, ValueError),
             dir_func = dir_func)

if __name__ == '__main__': fh.do_test_loop(test)
