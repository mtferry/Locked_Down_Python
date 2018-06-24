# Fuzz Tests for _pickle

import test.fuzzhelper as fh
import _pickle

def dir_func(i):
  d = dir(i)
  if 'memo' in d and fh.bool():
    setattr(i, 'persistent_id', fh.dict())
  if 'persistent_id' in d and fh.bool():
    setattr(i, 'persistent_id', fh.function())
  return d

def test():
  for _ in range(9999):
    fh.check(_pickle,
             valid_inputs = [
                            ((),{}),
                            ((fh.object,),{}),
                            ((fh.bytes, fh.bytes),{}),
                            ((fh.file_object, fh.bool, fh.bytes, fh.bytes),{}),
                            ((fh.object, fh.int, fh.bool),{}),
                            ((fh.object, fh.file_object, fh.int, fh.bool),{}),
                            ((fh.bytes, fh.bool, fh.bytes, fh.bytes),{}),
                            ((fh.file_object, fh.bool, fh.bytes, fh.bytes),{})
                            ],
             expected_exceptions = (TypeError, ValueError, AttributeError),
             dir_func = dir_func)

if __name__ == '__main__': fh.do_test_loop(test)
