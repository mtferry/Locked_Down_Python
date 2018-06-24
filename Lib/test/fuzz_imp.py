# Fuzz Tests for _imp

import test.fuzzhelper as fh
import _imp

def fh_code():
  return fh.function().__code__

def fh_spec():
  return type(fh.__spec__)(fh.str(),fh.str())
  
def fh_module():
  return type(fh)(fh.str())
  
def test():
  for _ in range(9999):
    fh.check(_imp,
             valid_inputs = [
                            ((),{}),
                            ((fh.str,),{}),
                            ((fh.bytes,),{}),
                            ((fh_code, fh.str),{}),
                            ((fh_spec,),{}),
                            ((fh_spec, fh.bool),{}),
                            ((fh_module,),{}),
                            ((fh.int, fh.bytes),{})
                            ],
             expected_exceptions = (TypeError, AttributeError, ImportError))

if __name__ == '__main__': fh.do_test_loop(test)
