# Fuzz Tests for pyexpat, _elementtree

import test.fuzzhelper as fh
import pyexpat, _elementtree

def fh_element(*a, **k):
  return _elementtree.Element(fh.str(), fh.dict())

def fh_element_list():
  return [fh_element() for _ in range(abs(fh.int()))]
  
def fh_dir_func(i):
  d = dir(i)
  if 'tag' in d and fh.bool():
    setattr(i, 'tag', fh.str())
  if 'text' in d and fh.bool():
    setattr(i, 'text', fh.str())
  if 'tail' in d and fh.bool():
    setattr(i, 'tail', fh.str())
  if 'attribute' in d and fh.bool():
    setattr(i, 'attribute', fh.dict())
  return d
  
def test():
  for _ in range(99):
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

    fh.check(_elementtree,
             valid_inputs = [
                             ((),{}),
                             ((fh.dict,),{}),
                             ((fh.str,),{}),
                             ((fh.str, fh.dict),{}),
                             ((fh.str, fh.function, fh.str),{}),
                             ((fh.object, fh.object),{}),
                             ((fh.str, fh.str, fh.str),{}),
                             ((fh.list, fh.list),{}),
                             ((fh_element,),{}),
                             ((fh.int, fh_element,),{}),
                             ((fh_element_list,),{}),
                             ((lambda: fh_element,),{}),
                             ((fh.file_object,),{}),
                             
                            ],
             expected_exceptions = (TypeError, ValueError, IndexError),
             dir_func = fh_dir_func)

if __name__ == '__main__': fh.do_test_loop(test)
